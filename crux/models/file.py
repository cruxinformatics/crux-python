"""Module contains File model."""

from typing import (  # noqa: F401 pylint: disable=unused-import
    Any,
    Dict,
    IO,
    Iterable,
    List,
    Union,
)

from google.resumable_media.common import InvalidResponse  # type: ignore
from google.resumable_media.requests import (  # type: ignore
    ChunkedDownload,
    ResumableUpload,
)

from crux._compat import unicode
from crux._utils import (
    DEFAULT_CHUNK_SIZE,
    get_signed_url_session,
    ResumableUploadSignedSession,
    valid_chunk_size,
)
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
            "POST", ["resources", self.id, "content-url"], headers=headers, json={}
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

    def iter_content(self, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (int) -> Iterable[str]
        """Streams the file resource.

        Args:
            chunk_size (int): Chunk Size for the stream.

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

        return data.iter_content(chunk_size=chunk_size)

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

    def _ul_signed_url_resumable(self, file_pointer, media_type):

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Upload-Content-Type": media_type,
        }

        upload_session_response = self.connection.api_call(
            "POST",
            ["resources", self.id, "upload-session-start"],
            headers=headers,
            json={},
        )

        upload_response_json = upload_session_response.json()

        signed_url = upload_response_json.get("signedURL").get("url")
        if not signed_url:
            raise KeyError(
                "Signed URL missing in response for resource {id}".format(id=self.id)
            )

        signed_url_headers = upload_response_json.get("signedURL").get("headers")

        if not signed_url_headers:
            raise KeyError(
                "Signed URL Headers missing in response for resource {id}".format(
                    id=self.id
                )
            )

        upload = ResumableUpload(signed_url, DEFAULT_CHUNK_SIZE)

        metadata = {"name": self.name}

        transport = get_signed_url_session(session_class=ResumableUploadSignedSession)

        transport.headers = signed_url_headers

        upload.initiate(
            transport, file_pointer, metadata, signed_url_headers["Content-Type"]
        )

        while not upload.finished:
            if upload.invalid:
                upload.recover(transport)
            upload.transmit_next_chunk(transport)

        payload = {"sessionId": upload_response_json.get("sessionId")}
        return self.connection.api_call(
            "POST",
            ["resources", self.id, "upload-session-complete"],
            headers=headers,
            json=payload,
        )

    def _upload(self, file_pointer, media_type):

        if self.connection.crux_config.only_use_crux_domains:
            headers = {"Content-Type": media_type, "Accept": "application/json"}
            return self.connection.api_call(
                "PUT",
                ["resources", self.id, "content"],
                data=file_pointer,
                headers=headers,
                model=File,
            )

        else:
            return self._ul_signed_url_resumable(file_pointer, media_type)

    def upload(self, local_path, media_type=None):
        # type: (Union[IO, str], str) -> File
        """Uploads the content to empty file resource.

        Args:
            local_path (str or file): Local OS path whose content is to be uploaded.
            media_type (str): Content type of the file. Defaults to None.

        Returns
            File: File model object.

        Raises:
            TypeError: If local_path type is invalid.
        """

        if hasattr(local_path, "read"):

            if media_type is None:
                media_type = MediaType.detect(getattr(local_path, "name"))

            upload_result = self._upload(local_path, media_type=media_type)

        elif isinstance(local_path, (str, unicode)):

            if media_type is None:
                media_type = MediaType.detect(local_path)

            with open(local_path, "rb") as file_pointer:
                upload_result = self._upload(file_pointer, media_type=media_type)

        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )

        if upload_result:
            # Refresh metadata to reflect actual size after uploading the file.
            raw_response = self._get_metadata()
            refreshed_object = File.from_dict(raw_response)
            refreshed_object.connection = self.connection
            refreshed_object.raw_response = raw_response
            return refreshed_object
        else:
            raise CruxClientError(
                "Unable to upload file {file_name} to path {path}".format(
                    file_name=self.name, path=self.path
                )
            )
