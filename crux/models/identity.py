"""Module contains Identity model."""

from typing import Any, Dict  # noqa: F401

from crux.models.model import CruxModel


class Identity(CruxModel):
    """Identity Model."""

    def __init__(self, object_model=None, connection=None):
        # type: (...) -> None
        """
        Attributes:
            identity_id (str): Identity_id. Defaults to None.
            parent_identity_id (str): Parent Identity ID. Defaults to None.
            description (str): Description. Defaults to None.
            company_name (str): Company Name. Defaults to None.
            first_name (str): First Name. Defaults to None.
            last_name (str): Last Name. Defaults to None.
            role (str): Role. Defaults to None.
            phone (str): Phone. Defaults to None.
            email (str): Email. Defaults to None.
            type (str): Type. Defaults to None.
            website (str): Website. Defaults to None.
            landing_page (str): Landing page. Defaults to None.
            connection (crux._client.CruxClient): Connection Object. Defaults to None.
            raw_response (dict): Response Content. Defaults to None.

        Raises:
            ValueError: If identity_id is none.
        """
        self.object_model = object_model
        self.connection = connection

    @property
    def identity_id(self):
        """str: Gets the Identity Id."""
        return self.object_model["identityId"]

    @property
    def parent_identity_id(self):
        """str: Gets the Parent Identity Id."""
        return self.object_model["parentIdentityId"]

    @property
    def company_name(self):
        """str: Gets the Company name."""
        return self.object_model["companyName"]

    @property
    def description(self):
        """str: Gets the Description."""
        return self.object_model["description"]

    @property
    def first_name(self):
        """str: Gets the First name."""
        return self.object_model["firstName"]

    @property
    def last_name(self):
        """str: Gets the Last name."""
        return self.object_model["lastName"]

    @property
    def role(self):
        """str: Gets the Role."""
        return self.object_model["role"]

    @property
    def email(self):
        """str: Gets the Email."""
        return self.object_model["email"]

    @property
    def website(self):
        """str: Gets the Website."""
        return self.object_model["website"]

    @property
    def landing_page(self):
        """str: Gets the Landing Page."""
        return self.object_model["landingPage"]

    @property
    def type(self):
        """str: Gets the Type."""
        return self.object_model["type"]

    @property
    def phone(self):
        """str: Gets the phone."""
        return self.object_model["phone"]

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Identity object to Identity Dictionary.

        Returns:
            dict: Identity Dictionary.
        """
        return self.object_model

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Identity
        """Transforms Identity Dictionary to Identity object.

        Args:
            a_dict (dict): Identity Dictionary.

        Returns:
            crux.models.Identity: Identity Object.
        """
        return cls(object_model=a_dict)
