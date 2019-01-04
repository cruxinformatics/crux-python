"""Module contains Table model."""

from typing import Any, Dict  # noqa: F401 pylint: disable=unused-import

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
            "labels": self.labels,
        }
