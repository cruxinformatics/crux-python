"""Module contains File model."""

from typing import Any, Dict, IO, Iterable, List, Union  # noqa: F401

from google.resumable_media.common import (  # type: ignore
    DataCorruption,
    InvalidResponse,
)
from google.resumable_media.requests import (  # type: ignore
    ChunkedDownload,
    ResumableUpload,
)
from requests.exceptions import (
    ConnectTimeout,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)

from crux._compat import unicode
from crux._utils import (
    create_logger,
    DEFAULT_CHUNK_SIZE,
    get_session,
    Headers,
    ResumableUploadSignedSession,
    valid_chunk_size,
)
from crux.exceptions import (
    CruxClientConnectionError,
    CruxClientError,
    CruxClientHTTPError,
    CruxClientTimeout,
    CruxClientTooManyRedirects,
)
from crux.models.resource import MediaType, Resource


log = create_logger(__name__)


class File(Resource):
    """File Model."""

    def _get_signed_url(self):
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        response = self.connection.api_call(
            "POST", ["resources", self.id, "content-url"], headers=headers, json={}
        )

        url = response.json().get("url")

        if not url:
            raise KeyError(
                "Signed URL missing in response for resource {id}".format(id=self.id)
            )

        return url

    def _dl_signed_url(self, file_obj, chunk_size=DEFAULT_CHUNK_SIZE):
        """Download from signed URL using requests directly, not google-resumable-media."""
        signed_url = self._get_signed_url()

        log.trace("Using direct signed url: %s", signed_url)

        transport = get_session(proxies=self.connection.crux_config.proxies)

        log.debug("Using Proxies %s for downloading", transport.proxies)

        try:
            with transport as session:
                response = session.get(signed_url, stream=True)
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=chunk_size):
                    file_obj.write(chunk)
        except HTTPError as err:
            raise CruxClientHTTPError(str(err), err.response)
        except TooManyRedirects as err:
            raise CruxClientTooManyRedirects(str(err))
        except (ProxyError, SSLError) as err:
            raise CruxClientConnectionError(str(err))
        except (ConnectTimeout, ReadTimeout) as err:
            raise CruxClientTimeout(str(err))

        return True

    def _dl_signed_url_resumable(self, file_obj, chunk_size=DEFAULT_CHUNK_SIZE):
        """Download from signed URL using google-resumable-media."""
        signed_url = self._get_signed_url()

        log.trace("Using resumable signed url: %s", signed_url)

        transport = get_session(proxies=self.connection.crux_config.proxies)

        log.debug("Using Proxies %s for downloading", transport.proxies)

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

        download = ChunkedDownload(signed_url, chunk_size, file_obj)

        log.debug("Starting download using signed url for resource %s", self.id)

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
                        log.debug(
                            "fetched_signed_urls count for download is %s",
                            fetched_signed_urls,
                        )
                        total_bytes_from_urls.append(0)
                        refreshes_without_progress += 1
                        log.debug(
                            "refreshes_without_progress count for download is %s",
                            refreshes_without_progress,
                        )
                        bytes_at_last_refresh = sum_total_bytes_from_urls
                    else:
                        # Exceeded max new signed URLs without progress
                        raise CruxClientError(
                            "Exceeded max new Signed URLs without progress"
                        )
                else:
                    refreshes_without_progress = 0
                    log.debug("Fetching new singed url")
                    new_signed_url = self._get_signed_url()
                    log.trace("New signed url: %s", new_signed_url)
                    fetched_signed_urls += 1
                    log.debug(
                        "fetched_signed_urls count for download is %s",
                        fetched_signed_urls,
                    )
                    total_bytes_from_urls.append(0)
                    bytes_at_last_refresh = sum_total_bytes_from_urls

                # Replace the download object with a new one, using a new signed URL,
                # but start where the last download object left off.
                log.debug(
                    "Resuming download with new_signed_url %s starting at %s bytes",
                    new_signed_url,
                    sum_total_bytes_from_urls,
                )
                download = ChunkedDownload(
                    new_signed_url,
                    chunk_size,
                    file_obj,
                    start=sum_total_bytes_from_urls,
                )
            except DataCorruption as err:
                raise CruxClientError(err)

        # Closing the session as it is not closed by Resumable Media Lib.
        transport.close()
        log.debug("Download completed using signed url for resource %s", self.id)

        return True

    def iter_content(self, chunk_size=DEFAULT_CHUNK_SIZE, only_use_crux_domains=None):
        # type: (int, bool) -> Iterable[str]
        """Streams the file resource.

        Args:
            chunk_size (int): Chunk Size for the stream.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Yields:
            bytes: Bytes of file resource.

        Raises:
            ValueError: If chunk_size is not multiple of 256 KiB.
        """

        headers = Headers({"accept": "*/*"})

        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        # If we must use only Crux domains, download via the API.
        if only_use_crux_domains is None:
            only_use_crux_domains = self.connection.crux_config.only_use_crux_domains

        if only_use_crux_domains:

            log.debug("Using Crux Domain for streaming file resource %s", self.id)
            data = self.connection.api_call(
                "GET", ["resources", self.id, "content"], headers=headers, stream=True
            )
            # Performing early return to avoid below computation
            return data.iter_content(chunk_size=chunk_size)

        log.debug("Using Resumable Signed url for streaming file resource %s", self.id)

        signed_url = self._get_signed_url()
        session = get_session(proxies=self.connection.crux_config.proxies)
        data = session.get(signed_url, stream=True)

        return data.iter_content(chunk_size=chunk_size)

    def _download_file(
        self, file_obj, chunk_size=DEFAULT_CHUNK_SIZE, only_use_crux_domains=None
    ):

        # If size is None it means the file has been created,
        # but no contents uploaded. This is similar to doing touch on command line,
        # it creates an empty file.
        # By returning True here we effectively "download" and write an empty file,
        # which matches file system mechanics of creating a file without writing contents
        if self.size is None:
            log.debug("File resource %s is of size None", self.id)
            return True

        # google-resumable-media has a bug where is expects the 'content-range' even
        # for 200 OK responses, which happens when the range is larger than the size.
        # There isn't much point in using resumable media for small files.
        # Make sure size is greater than 2x chunk_size if Google Resumable media is
        # to be used.
        small_enough = self.size < (chunk_size * 2)

        # If we must use only Crux domains, download via the API.
        if only_use_crux_domains is None:
            only_use_crux_domains = self.connection.crux_config.only_use_crux_domains

        if only_use_crux_domains:
            log.debug("Using Crux Domain for downloading file resource %s", self.id)
            return self._download(
                file_obj=file_obj, media_type=None, chunk_size=chunk_size
            )
        # Use requests directly for small files.
        elif small_enough:
            log.debug(
                "Using Direct Signed url for downloading file resource %s", self.id
            )
            return self._dl_signed_url(file_obj=file_obj, chunk_size=chunk_size)
        # Use google-resumable-media for large files
        else:
            log.debug(
                "Using Resumable Signed url for downloading file resource %s", self.id
            )
            return self._dl_signed_url_resumable(
                file_obj=file_obj, chunk_size=chunk_size
            )

    def download(self, dest, chunk_size=DEFAULT_CHUNK_SIZE, only_use_crux_domains=None):
        # type: (str, int, bool) -> bool
        """Downloads the file resource.

        Args:
            dest (str or file): Local OS path at which file resource will be downloaded.
            chunk_size (int): Number of bytes to be read in memory.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Returns:
            bool: True if it is downloaded.

        Raises:
            TypeError: If dest is not a file like or string type.
        """
        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        if hasattr(dest, "write"):
            return self._download_file(
                dest, chunk_size=chunk_size, only_use_crux_domains=only_use_crux_domains
            )
        elif isinstance(dest, (str, unicode)):
            with open(dest, "wb") as file_obj:
                return self._download_file(
                    file_obj,
                    chunk_size=chunk_size,
                    only_use_crux_domains=only_use_crux_domains,
                )
        else:
            raise TypeError("Invalid Data Type for dest: {}".format(type(dest)))

    def _ul_signed_url_resumable(self, file_obj, media_type):

        headers = Headers(
            {
                "content-type": "application/json",
                "accept": "application/json",
                "x-upload-content-type": media_type,
            }
        )

        upload_session_response = self.connection.api_call(
            "POST",
            ["resources", self.id, "upload-session-start"],
            headers=headers,
            json={},
        )
        log.debug("Fetched upload session url for resource %s", self.id)

        upload_response_json = upload_session_response.json()

        signed_url = upload_response_json.get("signedURL").get("url")
        if not signed_url:
            raise KeyError(
                "Signed URL missing in response for resource {id}".format(id=self.id)
            )

        log.trace("Using Resumable upload signed url: %s", signed_url)

        signed_url_headers = Headers(
            upload_response_json.get("signedURL").get("headers")
        )

        log.trace("Signed url headers: %s", signed_url_headers)

        if not signed_url_headers:
            raise KeyError(
                "Signed URL Headers missing in response for resource {id}".format(
                    id=self.id
                )
            )

        session_id = upload_response_json.get("sessionId")

        if not session_id:
            raise KeyError(
                "sessionId Header missing in response for resource {id}".format(
                    id=self.id
                )
            )

        upload = ResumableUpload(signed_url, DEFAULT_CHUNK_SIZE)

        metadata = {"name": self.name}

        transport = get_session(
            session_class=ResumableUploadSignedSession,
            proxies=self.connection.crux_config.proxies,
        )

        transport.headers = signed_url_headers

        log.debug("Using Proxies %s for uploading", transport.proxies)

        log.debug("Initiating upload for resource %s", self.id)

        upload.initiate(
            transport, file_obj, metadata, signed_url_headers["content-type"]
        )

        log.debug("Starting upload using signed url for resource %s", self.id)

        try:
            while not upload.finished:
                if upload.invalid:
                    upload.recover(transport)
                upload.transmit_next_chunk(transport)
        except InvalidResponse as err:
            raise CruxClientError(err)

        log.debug("Upload completed using signed url for resource %s", self.id)

        payload = {"sessionId": session_id}
        return self.connection.api_call(
            "POST",
            ["resources", self.id, "upload-session-complete"],
            headers=headers,
            json=payload,
        )

    def _upload(self, file_obj, media_type, only_use_crux_domains=None):

        if only_use_crux_domains is None:
            only_use_crux_domains = self.connection.crux_config.only_use_crux_domains

        if only_use_crux_domains:
            log.debug("Using Crux Domain for uploading file resource %s", self.id)
            headers = Headers(
                {"content-type": media_type, "accept": "application/json"}
            )
            return self.connection.api_call(
                "PUT",
                ["resources", self.id, "content"],
                data=file_obj,
                headers=headers,
                model=File,
            )

        else:
            log.debug("Using Signed url for uploading file resource %s", self.id)
            return self._ul_signed_url_resumable(file_obj, media_type)

    def upload(self, src, media_type=None, only_use_crux_domains=None):
        # type: (Union[IO, str], str, bool) -> File
        """Uploads the content to empty file resource.

        Args:
            src (str or file): Local OS path whose content is to be uploaded.
            media_type (str): Content type of the file. Defaults to None.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Returns
            File: File model object.

        Raises:
            TypeError: If src type is invalid.
        """

        if hasattr(src, "read"):

            if media_type is None:
                media_type = MediaType.detect(getattr(src, "name"))

            upload_result = self._upload(
                src, media_type=media_type, only_use_crux_domains=only_use_crux_domains
            )

        elif isinstance(src, str):

            if media_type is None:
                media_type = MediaType.detect(src)

            with open(src, "rb") as file_obj:
                upload_result = self._upload(
                    file_obj,
                    media_type=media_type,
                    only_use_crux_domains=only_use_crux_domains,
                )

        else:
            raise TypeError("Invalid Data Type for source path: {}".format(type(src)))

        if upload_result:
            # Refresh metadata to reflect actual size after uploading the file.
            if self.refresh():
                return self
            else:
                raise CruxClientError(
                    "Error refreshing metadata for resource {id}".format(id=self.id)
                )
        else:
            raise CruxClientError(
                "Unable to upload file {file_name} to path {path}".format(
                    file_name=self.name, path=self.path
                )
            )
