"""Module contains Label model."""

from typing import Any, Dict

from crux._client import CruxClient
from crux._config import CruxConfig
from crux.models.model import CruxModel


class Label(CruxModel):
    """Label Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self.connection = (
            connection if connection is not None else CruxClient(CruxConfig(api_key=""))
        )

    @property
    def label_key(self):
        """str: Gets the Label Key."""
        return self.raw_model["labelKey"]

    @property
    def label_value(self):
        """str: Gets the Label Value."""
        return self.raw_model["labelValue"]

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Label object to Label Dictionary.

        Returns:
            dict: Label Dictionary.
        """
        return self.raw_model

    @classmethod
    def from_dict(cls, a_dict, connection=None):
        # type: (Dict[str,str], CruxClient) -> Label
        """Transforms Label Dictionary to Label object.

        Args:
            a_dict (dict): Label Dictionary.
            connection (CruxClient): Connection Object. Defaults to None.

        Returns:
            crux.models.Label: Label Object.
        """
        return cls(raw_model=a_dict, connection=connection)
