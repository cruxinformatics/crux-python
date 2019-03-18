"""Module contains Label model."""

from typing import Any, Dict, Optional  # noqa: F401

from crux.models.model import CruxModel


class Label(CruxModel):
    """Label Model."""

    def __init__(self, label_key=None, label_value=None):
        # type: (str, str) -> None
        """
        Attributes:
            label_key (str): Label Key. Defaults to None.
            label_value (str): Label value. Defaults to None.
        """
        self.label_key = label_key
        self.label_value = label_value

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Label object to Label Dictionary.

        Returns:
            dict: Label Dictionary.
        """
        return {"labelKey": self.label_key, "labelValue": self.label_value}

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str,str]) -> Label
        """Transforms Label Dictionary to Label object.

        Args:
            a_dict (dict): Label Dictionary.

        Returns:
            crux.models.Label: Label Object.
        """
        label_key = a_dict["labelKey"]
        label_value = a_dict["labelValue"]

        return cls(label_key=label_key, label_value=label_value)
