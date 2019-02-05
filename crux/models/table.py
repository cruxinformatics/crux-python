"""Module contains Table model."""

from typing import Any, Dict  # noqa: F401 pylint: disable=unused-import

from crux._compat import unicode
from crux._utils import DEFAULT_CHUNK_SIZE
from crux.models.resource import Resource


class Table(Resource):
    """Table model."""

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Table object to Table Dictionary.

        Returns:
            dict: Table Dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "type": self.type,
            "config": self.config,
            "folder": self.folder,
        }

    def download(self, local_path, media_type, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (str, str, int) -> bool
        """Downloads the table resource.

        Args:
            local_path (str or file): Local OS path at which file resource will be downloaded.
            media_type (str): Content Type for download.
            chunk_size (int): Number of bytes to be read in memory.

        Returns:
            bool: True if it is downloaded.

        Raises:
            TypeError: If local_path is not a file like or string type.
        """
        if hasattr(local_path, "write"):
            return self._download(
                local_path, media_type=media_type, chunk_size=chunk_size
            )
        elif isinstance(local_path, (str, unicode)):
            with open(local_path, "wb") as file_pointer:
                return self._download(
                    file_pointer, media_type=media_type, chunk_size=chunk_size
                )
        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )
