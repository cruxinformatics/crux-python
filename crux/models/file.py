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
from requests import Session

from crux.compat import unicode
from crux.exceptions import CruxClientError
from crux.models.resource import Resource
from crux.utils import ContentType, DEFAULT_CHUNK_SIZE, valid_chunk_size


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
            "labels": self.labels,
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

    def _dl_via_api(self, local_path, content_type, chunk_size=DEFAULT_CHUNK_SIZE):

        if content_type is not None:
            headers = {"Accept": content_type}
        else:
            headers = None

        data = self.connection.api_call(
            "GET", ["resources", self.id, "content"], headers=headers, stream=True
        )

        if hasattr(local_path, "write"):
            for chunk in data.iter_content(chunk_size=chunk_size):
                local_path.write(chunk)
            local_path.flush()
            return True
        elif isinstance(local_path, (str, unicode)):
            with open(local_path, mode="wb") as local_file:
                for chunk in data.iter_content(chunk_size=chunk_size):
                    local_file.write(chunk)
            return True
        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )

    def _dl_signed_url_resumable(  # pylint: disable=too-many-branches
        self, local_path, chunk_size=DEFAULT_CHUNK_SIZE
    ):

        if hasattr(local_path, "write"):
            local_file_object = local_path
        elif isinstance(local_path, (str, unicode)):
            local_file_object = open(local_path, "wb")
        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )
        signed_url = self._get_signed_url()
        transport = Session()
        bytes_at_last_refresh = 0
        refreshes_without_progress = 0
        fetched_signed_urls = 0
        total_bytes_downloaded = 0
        max_url_refreshes_without_progress = 5
        max_url_refreshes = 10

        download = ChunkedDownload(signed_url, chunk_size, local_file_object)

        while not download.finished:
            try:
                download.consume_next_chunk(transport)
                total_bytes_downloaded += download.bytes_downloaded
            except InvalidResponse:
                if total_bytes_downloaded <= bytes_at_last_refresh:
                    if refreshes_without_progress <= max_url_refreshes_without_progress:
                        if fetched_signed_urls <= max_url_refreshes:
                            new_signed_url = self._get_signed_url()
                            fetched_signed_urls += 1
                        else:
                            raise CruxClientError("Exceeded max new Signed URLs")
                        refreshes_without_progress += 1
                        total_bytes_downloaded += download.bytes_downloaded
                        bytes_at_last_refresh = total_bytes_downloaded
                    else:
                        raise CruxClientError(
                            "Exceeded max new Signed URLs without progress"
                        )
                else:
                    refreshes_without_progress = 0
                    if fetched_signed_urls <= max_url_refreshes:
                        new_signed_url = self._get_signed_url()
                        fetched_signed_urls += 1
                    else:
                        raise CruxClientError("Exceeded max new Signed URLs")
                    total_bytes_downloaded += download.bytes_downloaded
                    bytes_at_last_refresh = total_bytes_downloaded
                download = ChunkedDownload(
                    new_signed_url,
                    chunk_size,
                    local_file_object,
                    start=download.bytes_downloaded,
                )
        local_file_object.flush()
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

    def download(self, local_path, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (str, int) -> bool
        """Downloads the file resource.

        Args:
            local_path (str or file): Local OS path at which file resource will be downloaded.
            chunk_size (int): Number of bytes to be read in memory.

        Returns:
            bool: True if it is downloaded.

        Raises:
            ValueError: If chunk_size is not multiple of 256 KiB.
        """
        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        # google-resumable-media has a bug where is expects the 'content-range' even
        # for 200 OK responses, which happens when the range is larger than the size.
        # There isn't much point in using resumable media for small files.
        # Make sure size is greater than 2x chunk_size if Google Resumable media is
        # to be used.
        small_enough = self.size < (chunk_size * 2)

        if self.connection.crux_config.only_use_crux_domains or small_enough:
            return self._dl_via_api(
                local_path=local_path, content_type=None, chunk_size=chunk_size
            )
        else:
            return self._dl_signed_url_resumable(
                local_path=local_path, chunk_size=chunk_size
            )

    def upload(self, local_path, content_type=None):
        # type: (Union[IO, str], str) -> bool
        """Uploads the content to empty file resource.

        Args:
            local_path (str or file): Local OS path whose content is to be uploaded.
            content_type (str): Content type of the file. Defaults to None.

        Returns
            bool: True if it is uploaded.

        Raises:
            TypeError: If local_path type is invalid.
        """

        if hasattr(local_path, "read"):

            if content_type is None:
                content_type = ContentType.detect(getattr(local_path, "name"))

            headers = {"Content-Type": content_type, "Accept": "application/json"}

            resp = self.connection.api_call(
                "PUT",
                ["resources", self.id, "content"],
                data=local_path,
                headers=headers,
            )

            return resp.status_code == 200

        elif isinstance(local_path, str):

            if content_type is None:
                content_type = ContentType.detect(local_path)

            headers = {"Content-Type": content_type, "Accept": "application/json"}

            with open(local_path, mode="rb") as data:
                resp = self.connection.api_call(
                    "PUT", ["resources", self.id, "content"], data=data, headers=headers
                )

            return resp.status_code == 200

        else:
            raise TypeError("Invalid Data Type for local_path")
