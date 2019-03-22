"""Module contains Identity model."""

from typing import Any, Dict  # noqa: F401

from crux.models.model import CruxModel


class Identity(CruxModel):
    """Identity Model."""

    def __init__(
        self,
        identity_id=None,  # type: str
        parent_identity_id=None,  # type: str
        description=None,  # type: str
        company_name=None,  # type: str
        first_name=None,  # type: str
        last_name=None,  # type: str
        role=None,  # type: str
        phone=None,  # type: str
        email=None,  # type: str
        type=None,  # type: str # type name is by design pylint: disable=redefined-builtin
        website=None,  # type: str
        landing_page=None,  # type: str
        connection=None,
        raw_response=None,  # type: Dict[Any, Any]
    ):
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
        self._identity_id = identity_id
        self._parent_identity_id = parent_identity_id
        self._description = description
        self._company_name = company_name
        self._first_name = first_name
        self._last_name = last_name
        self._role = role
        self._phone = phone
        self._email = email
        self._type = type
        self._website = website
        self._landing_page = landing_page

        self.connection = connection
        self.raw_response = raw_response

    @property
    def identity_id(self):
        """str: Gets the Identity Id."""
        return self._identity_id

    @property
    def parent_identity_id(self):
        """str: Gets the Parent Identity Id."""
        return self._parent_identity_id

    @property
    def company_name(self):
        """str: Gets the Company name."""
        return self._company_name

    @property
    def description(self):
        """str: Gets the Description."""
        return self._description

    @property
    def first_name(self):
        """str: Gets the First name."""
        return self._first_name

    @property
    def last_name(self):
        """str: Gets the Last name."""
        return self._last_name

    @property
    def role(self):
        """str: Gets the Role."""
        return self._role

    @property
    def email(self):
        """str: Gets the Email."""
        return self._email

    @property
    def website(self):
        """str: Gets the Website."""
        return self._website

    @property
    def landing_page(self):
        """str: Gets the Landing Page."""
        return self._landing_page

    @property
    def type(self):
        """str: Gets the Type."""
        return self._type

    @property
    def phone(self):
        """str: Gets the phone."""
        return self._phone

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Identity object to Identity Dictionary.

        Returns:
            dict: Identity Dictionary.
        """
        return {
            "identityId": self.identity_id,
            "parentIdentityId": self.parent_identity_id,
            "description": self.description,
            "companyName": self.company_name,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "role": self.role,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "landingPage": self.landing_page,
            "type": self.type,
        }

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, str]) -> Identity
        """Transforms Identity Dictionary to Identity object.

        Args:
            a_dict (dict): Identity Dictionary.

        Returns:
            crux.models.Identity: Identity Object.
        """
        identity_id = a_dict["identityId"]
        # parent_identity_id = a_dict["parentIdentityId"]
        description = a_dict["description"]
        company_name = a_dict["companyName"]
        first_name = a_dict["firstName"]
        last_name = a_dict["lastName"]
        role = a_dict["role"]
        phone = a_dict["phone"]
        website = a_dict["website"]
        email = a_dict["email"]
        website = a_dict["website"]
        landing_page = a_dict["landingPage"]
        type = a_dict[  # type name is by design pylint: disable=redefined-builtin
            "type"
        ]

        return cls(
            identity_id=identity_id,
            description=description,
            company_name=company_name,
            first_name=first_name,
            last_name=last_name,
            role=role,
            phone=phone,
            email=email,
            website=website,
            landing_page=landing_page,
            type=type,
        )
