"""Module contains Label model."""

from typing import Any, Dict

from crux.models.model import CruxModel


class Label(CruxModel):
    """Label Model."""

    def __init__(self, raw_model=None):
        # type: (Dict) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}

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
    def from_dict(cls, a_dict):
        # type: (Dict[str,str]) -> Label
        """Transforms Label Dictionary to Label object.

        Args:
            a_dict (dict): Label Dictionary.

        Returns:
            crux.models.Label: Label Object.
        """
        return cls(raw_model=a_dict)
