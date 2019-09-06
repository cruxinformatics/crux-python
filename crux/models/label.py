"""Module contains Label model."""

from typing import Any, Dict, List

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


class LabelProxy(dict):
    # type() -> None
    """Maps data from and to API models"""

    def __delitem__(self, key):
        raise RuntimeError("Removal of key not allowed")

    def pop(self, key):
        raise RuntimeError("Removal of key not allowed")

    def popitem(self):
        raise RuntimeError("Removal of key not allowed")

    @classmethod
    def to_dict(cls, labels):
        # type: (List[Dict[str,str]]) -> Dict[str,str]
        """Converts API to Raw Model

        Args:
            labels (dict): API Model Label dictionary.

        Returnes:
            dict: Raw Model Label dictionary
        """
        labels_dict = cls()
        for label in labels:
            labels_dict[label["labelKey"]] = label["labelValue"]
        return labels_dict

    @classmethod
    def to_api_model(cls, labels):
        # type: (Dict[str,str]) -> List[Dict[str,str]]
        """Converts Raw to API Model

        Args:
            labels (dict): Raw Model Label dictionary.

        Returnes:
            dict: API Model Label dictionary
        """
        labels_list = []
        for label in labels:
            labels_list.append({"labelKey": label, "labelValue": labels[label]})
        return labels_list
