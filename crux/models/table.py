"""Module contains Table model."""

import logging
from typing import Any, Dict  # noqa: F401

from crux._compat import unicode
from crux._utils import DEFAULT_CHUNK_SIZE
from crux.models.resource import Resource


log = logging.getLogger(__name__)


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

    def download(self, dest, media_type, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (str, str, int) -> bool
        """Downloads the table resource.

        Args:
            dest (str or file): Local OS path at which file resource will be downloaded.
            media_type (str): Content Type for download.
            chunk_size (int): Number of bytes to be read in memory.

        Returns:
            bool: True if it is downloaded.

        Raises:
            TypeError: If dest is not a file like or string type.
        """
        if hasattr(dest, "write"):
            return self._download(dest, media_type=media_type, chunk_size=chunk_size)
        elif isinstance(dest, (str, unicode)):
            with open(dest, "wb") as file_obj:
                return self._download(
                    file_obj, media_type=media_type, chunk_size=chunk_size
                )
        else:
            raise TypeError("Invalid Data Type for dest: {}".format(type(dest)))
