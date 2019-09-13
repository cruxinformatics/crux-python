"""Module contains Permission model."""

from typing import Dict  # noqa: F401

from crux._client import CruxClient
from crux._config import CruxConfig
from crux.models.model import CruxModel


class Permission(CruxModel):
    """Permission Model."""

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
    def from_dict(cls, a_dict, connection=None):
        # type: (Dict[str, str], CruxClient) -> Permission
        """Transforms Dataset Dictionary to Dataset object.

        Args:
            a_dict (dict): Dataset Dictionary.
            connection (CruxClient): Connection Object. Defaults to None.
        Returns:
            crux.models.Permission: Permission Object.
        """
        return cls(raw_model=a_dict, connection=connection)
