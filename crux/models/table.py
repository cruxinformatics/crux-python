"""Module contains Table model."""

from typing import Any, Dict  # noqa: F401 pylint: disable=unused-import

from crux.models.resource import Resource


class Table(Resource):
    """Table model."""

    @property
    def folder(self):
        """str: Gets and Sets the folder."""
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = folder

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
            "folder": self.folder,
            "type": self.type,
            "config": self.config,
            "labels": self.labels,
        }
