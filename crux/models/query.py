"""Module contains Query model."""

from typing import Any, Dict, Iterable  # noqa: F401 pylint: disable=unused-import

from crux._utils import DEFAULT_CHUNK_SIZE, Headers, valid_chunk_size
from crux.models.resource import Resource


class Query(Resource):
    """Query Model."""

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Query object to Query dictionary.

        Returns:
            dict: Query dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "type": self.type,
            "config": self.config,
            "folder": self.folder,
        }

    def run(
        self,
        format="csv",  # type: str # format name is by design pylint: disable=redefined-builtin
        params=None,  # type: Dict[str, str]
        chunk_size=DEFAULT_CHUNK_SIZE,  # type: int
        decode_unicode=False,  # type: bool
    ):
        # type(...) -> Iterable[str]
        """Method which streams the Query

        Args:
            format (str): Output format of the query. Defaults to csv.
            params (dict): Run parameters. Defaults to None.
            chunk_size (int): Chunk Size for the stream
            decode_unicode (bool): If decode_unicode is True,content will be decoded using the
                best available encoding based on the response.
                Defaults to False.

        Yields:
            bytes: Bytes of content.

        Raises:
            ValueError: If chunk size is not multiple of 256 KiB.
        """

        params = params if params else {}

        headers = Headers({"content-type": "application/json", "accept": "*/*"})

        params["format"] = format

        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        data = self.connection.api_call(
            "GET",
            ["resources", self.id, "content"],
            params=params,
            stream=True,
            headers=headers,
        )

        return data.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode)

    def download(
        self, dest, format="csv", params=None
    ):  # It is by design pylint: disable=redefined-builtin
        # type: (str, str, Dict[Any, Any]) -> bool
        """Method which streams the Query

        Args:
            dest (str): Local OS path at which resource will be downloaded.
            media_type (str): Output format of the query. Defaults to csv.
            params (dict): Run parameters. Defaults to None.

        Returns:
            bool: True if it is downloaded.
        """

        params = params if params else {}
        params["format"] = format
        headers = Headers({"content-type": "application/json", "accept": "*/*"})
        data = self.connection.api_call(
            "GET",
            ["resources", self.id, "content"],
            params=params,
            stream=True,
            headers=headers,
        )

        with open(dest, "w") as local_file:
            for line in data.iter_lines():
                if line:
                    dcd_line = line.decode("utf-8")
                    local_file.write(dcd_line + "\n")
        data.close()
        return True
