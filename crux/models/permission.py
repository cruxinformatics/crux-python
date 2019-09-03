"""Module contains Permission model."""

from typing import Dict  # noqa: F401

from crux.models.model import CruxModel


class Permission(CruxModel):
    """Permission Model."""

    def __init__(self, raw_model=None):
        # type: (Dict) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}

    @property
    def target_id(self):
        """str: Gets the Target ID."""
        return self.raw_model["targetId"]

    @property
    def identity_id(self):
        """str: Gets the Identity ID."""
        return self.raw_model["identityId"]

    @property
    def permission_name(self):
        """str: Gets the Permission Name."""
        return self.raw_model["permissionName"]

    def to_dict(self):
        # type: () -> Dict[str, str]
        """Transforms Dataset object to Dataset Dictionary.

        Returns:
            dict: Dataset Dictionary.
        """
        return self.raw_model

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Permission
        """Transforms Dataset Dictionary to Dataset object.

        Args:
            a_dict (dict): Dataset Dictionary.

        Returns:
            crux.models.Permission: Permission Object.
        """
        return cls(raw_model=a_dict)
