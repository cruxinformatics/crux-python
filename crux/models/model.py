"""Module defines abstract CruxModel."""

import copy
import pprint
from typing import Any, Dict  # noqa: F401

from crux._client import CruxClient
from crux._client import CruxConfig


class CruxModel(object):
    """Base Crux model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Resource raw dictionary. Defaults to None.
            connection (CruxClient): Connection object. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self._connection = connection

    @property
    def connection(self):
        """CruxClient: API connection client."""
        if self._connection is None:
            self._connection = CruxClient(CruxConfig())

        return self._connection

    @connection.setter
    def connection(self, connection):
        self._connection = connection

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Returns dict copy of raw model.

        Returns:
            dict: Raw model dict.
        """

        # Deep copy raw_model, otherwise if a user modifies the returned dict,
        # they will be mutating this instances raw_model.
        return copy.deepcopy(self.raw_model)

    @classmethod
    def from_dict(cls, a_dict, connection=None):
        # type: (Dict[str, Any], CruxClient) -> Any
        """Returns model instance created from raw model dict.

        Args:
            a_dict (dict): Model dict.
            connection (CruxClient): Connection bbject. Defaults to None.

        Returns:
            crux.models.model.CruxModel: Model instance.
        """

        return cls(raw_model=a_dict, connection=connection)

    def to_str(self):
        # type: () -> str
        """Absract to_str method."""
        return pprint.pformat(self.raw_model)

    def __repr__(self):
        # type: () -> str
        """Absract __repr__ method."""
        return self.to_str()
