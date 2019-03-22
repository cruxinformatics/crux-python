"""Module contains Permission model."""

from typing import Dict  # noqa: F401

from crux.models.model import CruxModel


class Permission(CruxModel):
    """Permission Model."""

    def __init__(self, target_id=None, identity_id=None, permission_name=None):
        # type(str, str, str) -> None
        """
        Attributes:
            target_id (str): Target ID. Defaults to None.
            identity_id (str): Identity ID. Defaults to None.
            permission_name (str): Permission name. Defaults to None.
        """
        self._target_id = target_id
        self._identity_id = identity_id
        self._permission_name = permission_name

    @property
    def target_id(self):
        """str: Gets the Target ID."""
        return self._target_id

    @property
    def identity_id(self):
        """str: Gets the Identity ID."""
        return self._identity_id

    @property
    def permission_name(self):
        """str: Gets the Permission Name."""
        return self._permission_name

    def to_dict(self):
        # type: () -> Dict[str, str]
        """Transforms Dataset object to Dataset Dictionary.

        Returns:
            dict: Dataset Dictionary.
        """
        return {
            "targetId": self.target_id,
            "identityId": self.identity_id,
            "permissionName": self.permission_name,
        }

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Permission
        """Transforms Dataset Dictionary to Dataset object.

        Args:
            a_dict (dict): Dataset Dictionary.

        Returns:
            crux.models.Permission: Permission Object.
        """
        target_id = a_dict["targetId"]
        identity_id = a_dict["identityId"]
        permission_name = a_dict["permissionName"]

        return cls(
            target_id=target_id,
            identity_id=identity_id,
            permission_name=permission_name,
        )
