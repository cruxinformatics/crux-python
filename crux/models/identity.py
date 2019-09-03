"""Module contains Identity model."""

from typing import Any, Dict  # noqa: F401

from crux._client import CruxClient
from crux._config import CruxConfig
from crux.models.model import CruxModel


class Identity(CruxModel):
    """Identity Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Identity raw dictionary. Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        Raises:
            ValueError: If name or tags are set to None.
        """
        self.raw_model = raw_model if raw_model is not None else {}
        self.connection = (
            connection if connection is not None else CruxClient(CruxConfig())
        )

    @property
    def identity_id(self):
        """str: Gets the Identity Id."""
        return self.raw_model["identityId"]

    @property
    def parent_identity_id(self):
        """str: Gets the Parent Identity Id."""
        return self.raw_model["parentIdentityId"]

    @property
    def company_name(self):
        """str: Gets the Company name."""
        return self.raw_model["companyName"]

    @property
    def description(self):
        """str: Gets the Description."""
        return self.raw_model["description"]

    @property
    def first_name(self):
        """str: Gets the First name."""
        return self.raw_model["firstName"]

    @property
    def last_name(self):
        """str: Gets the Last name."""
        return self.raw_model["lastName"]

    @property
    def role(self):
        """str: Gets the Role."""
        return self.raw_model["role"]

    @property
    def email(self):
        """str: Gets the Email."""
        return self.raw_model["email"]

    @property
    def website(self):
        """str: Gets the Website."""
        return self.raw_model["website"]

    @property
    def landing_page(self):
        """str: Gets the Landing Page."""
        return self.raw_model["landingPage"]

    @property
    def type(self):
        """str: Gets the Type."""
        return self.raw_model["type"]

    @property
    def phone(self):
        """str: Gets the phone."""
        return self.raw_model["phone"]

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Identity object to Identity Dictionary.

        Returns:
            dict: Identity Dictionary.
        """
        return self.raw_model

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Identity
        """Transforms Identity Dictionary to Identity object.

        Args:
            a_dict (dict): Identity Dictionary.

        Returns:
            crux.models.Identity: Identity Object.
        """
        return cls(raw_model=a_dict)
