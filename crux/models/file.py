"""Module contains File model."""

from typing import (  # noqa: F401 pylint: disable=unused-import
    Any,
    Dict,
    IO,
    Iterable,
    List,
    Union,
)

from crux.models.resource import Resource
from crux.utils import ContentType, DEFAULT_CHUNK_SIZE, valid_chunk_size


class File(Resource):
    """File Model."""

    @property
    def folder(self):
        """str: Gets and Sets the folder."""
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = folder

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
            "folder": self.folder,
            "type": self.type,
            "labels": self.labels,
        }

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

    def download(
        self, local_path, chunk_size=DEFAULT_CHUNK_SIZE
    ):  # content_type is skipped intentionally pylint: disable=arguments-differ
        # type: ignore # https://github.com/python/mypy/issues/3750
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

        return self._download(
            local_path=local_path, content_type=None, chunk_size=chunk_size
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
