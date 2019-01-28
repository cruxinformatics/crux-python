"""Module contains File model."""

import json
from typing import (  # noqa: F401 pylint: disable=unused-import
    Any,
    Dict,
    IO,
    Iterable,
    List,
    Union,
)

from google.resumable_media.common import InvalidResponse  # type: ignore
from google.resumable_media.requests import ChunkedDownload  # type: ignore

from crux._compat import unicode
from crux._utils import DEFAULT_CHUNK_SIZE, get_signed_url_session, valid_chunk_size
from crux.exceptions import CruxClientError
from crux.models.resource import MediaType, Resource


class File(Resource):
    """File Model."""

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms File object to File Dictionary.

        Returns:
            dict: File Dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "type": self.type,
            "folder": self.folder,
        }

    def _get_signed_url(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = self.connection.api_call(
            "POST",
            ["resources", self.id, "content-url"],
            headers=headers,
            data=json.dumps({}),
        )

        url = response.json().get("url")

        if not url:
            raise KeyError(
                "Signed URL missing in response for resource {id}".format(id=self.id)
            )

        return url

    def _dl_signed_url_resumable(self, file_pointer, chunk_size=DEFAULT_CHUNK_SIZE):

        signed_url = self._get_signed_url()

        transport = get_signed_url_session()

        # Track how many bytes the client has downloaded since the last time they
        # got a new signed URL, and how many times that got a new URL without
        # downloading more bytes.
        # This is to prevent infinite loops without progress.
        bytes_at_last_refresh = 0
        refreshes_without_progress = 0
        # Track how much has been downloaded from each signed URL
        total_bytes_from_urls = [0]
        fetched_signed_urls = 0
        max_url_refreshes_without_progress = 5
        max_url_refreshes = 100

        download = ChunkedDownload(signed_url, chunk_size, file_pointer)

        while not download.finished:
            try:
                # This downloads a chunk and writes it to file_object
                download.consume_next_chunk(transport)
                total_bytes_from_urls[-1] = download.bytes_downloaded
            # Catch the signed URL expiring
            except InvalidResponse:
                # Limit total new URL(s)
                if fetched_signed_urls >= max_url_refreshes:
                    raise CruxClientError("Exceeded max new Signed URLs")
                sum_total_bytes_from_urls = sum(total_bytes_from_urls)
                # Check if download has made progress downloading since last time we got URL
                if not sum_total_bytes_from_urls > bytes_at_last_refresh:
                    # Limit new URLs without making progress downloading
                    if refreshes_without_progress <= max_url_refreshes_without_progress:
                        new_signed_url = self._get_signed_url()
                        fetched_signed_urls += 1
                        total_bytes_from_urls.append(0)
                        refreshes_without_progress += 1
                        bytes_at_last_refresh = sum_total_bytes_from_urls
                    else:
                        # Exceeded max new signed URLs without progress
                        raise CruxClientError(
                            "Exceeded max new Signed URLs without progress"
                        )
                else:
                    refreshes_without_progress = 0
                    new_signed_url = self._get_signed_url()
                    fetched_signed_urls += 1
                    total_bytes_from_urls.append(0)
                    bytes_at_last_refresh = sum_total_bytes_from_urls

                # Replace the download object with a new one, using a new signed URL,
                # but start where the last download object left off.
                download = ChunkedDownload(
                    new_signed_url,
                    chunk_size,
                    file_pointer,
                    start=sum_total_bytes_from_urls,
                )
        return True

    def iter_content(self, chunk_size=DEFAULT_CHUNK_SIZE, decode_unicode=False):
        # type: (int, bool) -> Iterable[str]
        """Streams the file resource.

        Args:
            chunk_size (int): Chunk Size for the stream.
            decode_unicode (bool): If decode_unicode is True, content will be decoded using the
                best available encoding based on the response.

        Yields:
            bytes: Bytes of file resource.

        Raises:
            ValueError: If chunk_size is not multiple of 256 KiB.
        """
        headers = {"Accept": "*/*"}

        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        data = self.connection.api_call(
            "GET", ["resources", self.id, "content"], headers=headers, stream=True
        )

        return data.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode)

    def _download_file(self, file_pointer, chunk_size=DEFAULT_CHUNK_SIZE):
        # google-resumable-media has a bug where is expects the 'content-range' even
        # for 200 OK responses, which happens when the range is larger than the size.
        # There isn't much point in using resumable media for small files.
        # Make sure size is greater than 2x chunk_size if Google Resumable media is
        # to be used.
        small_enough = self.size < (chunk_size * 2)

        if self.connection.crux_config.only_use_crux_domains or small_enough:
            return self._download(
                file_pointer=file_pointer, media_type=None, chunk_size=chunk_size
            )
        else:
            return self._dl_signed_url_resumable(
                file_pointer=file_pointer, chunk_size=chunk_size
            )

    def download(self, local_path, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (str, int) -> bool
        """Downloads the file resource.

        Args:
            local_path (str or file): Local OS path at which file resource will be downloaded.
            chunk_size (int): Number of bytes to be read in memory.

        Returns:
            bool: True if it is downloaded.

        Raises:
            TypeError: If local_path is not a file like or string type.
        """
        if hasattr(local_path, "write"):
            return self._download_file(local_path, chunk_size=chunk_size)
        elif isinstance(local_path, (str, unicode)):
            with open(local_path, "wb") as file_pointer:
                return self._download_file(file_pointer, chunk_size=chunk_size)
        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )

    def upload(self, local_path, media_type=None):
        # type: (Union[IO, str], str) -> bool
        """Uploads the content to empty file resource.

        Args:
            local_path (str or file): Local OS path whose content is to be uploaded.
            media_type (str): Content type of the file. Defaults to None.

        Returns
            bool: True if it is uploaded.

        Raises:
            TypeError: If local_path type is invalid.
        """

        if hasattr(local_path, "read"):

            if media_type is None:
                media_type = MediaType.detect(getattr(local_path, "name"))

            headers = {"Content-Type": media_type, "Accept": "application/json"}

            resp = self.connection.api_call(
                "PUT",
                ["resources", self.id, "content"],
                data=local_path,
                headers=headers,
            )

            return resp.status_code == 200

        elif isinstance(local_path, str):

            if media_type is None:
                media_type = MediaType.detect(local_path)

            headers = {"Content-Type": media_type, "Accept": "application/json"}

            with open(local_path, mode="rb") as data:
                resp = self.connection.api_call(
                    "PUT", ["resources", self.id, "content"], data=data, headers=headers
                )

            return resp.status_code == 200

        else:
            raise TypeError("Invalid Data Type for local_path")
