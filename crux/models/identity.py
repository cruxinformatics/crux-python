"""Module contains Identity model."""

from typing import Any, Dict  # noqa: F401 pylint: disable=unused-import

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
            connection (crux.client.CruxClient): Connection Object. Defaults to None.
            raw_response (dict): Response Content. Defaults to None.

        Raises:
            ValueError: If identity_id is none.
        """
        self._identity_id = None
        self._parent_identity_id = None
        self._api_key = None
        self._bucket_name = None
        self._description = None
        self._company_name = None
        self._first_name = None
        self._last_name = None
        self._role = None
        self._phone = None
        self._image_name = None
        self._image_url = None
        self._email = None
        self._type = None
        self._website = None
        self._landing_page = None

        self.identity_id = identity_id
        self.parent_identity_id = parent_identity_id
        self.description = description
        self.company_name = company_name
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.phone = phone
        self.email = email
        self.type = type
        self.website = website
        self.landing_page = landing_page
        self.connection = connection
        self.raw_response = raw_response

    @property
    def identity_id(self):
        """str: Gets and Sets the Identity Id."""
        return self._identity_id

    @identity_id.setter
    def identity_id(self, identity_id):
        if identity_id is None:
            raise ValueError("identity_id should not be none")
        self._identity_id = identity_id

    @property
    def parent_identity_id(self):
        """str: Gets and Sets the Parent Identity Id"""
        return self._parent_identity_id

    @parent_identity_id.setter
    def parent_identity_id(self, parent_identity_id):
        self._parent_identity_id = parent_identity_id

    @property
    def company_name(self):
        """str: Gets and Sets the Company name"""
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        self._company_name = company_name

    @property
    def description(self):
        """str: Gets and Sets the Description."""
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def first_name(self):
        """str: Gets and Sets the First name."""
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @property
    def last_name(self):
        """str: Gets and Sets the Last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @property
    def role(self):
        """str: Gets and Sets the Role."""
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    @property
    def image_name(self):
        """str: Gets and Sets the Image name."""
        return self._image_name

    @property
    def email(self):
        """str: Gets and Sets the Email."""
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def website(self):
        """str: Gets and Sets the Website."""
        return self._website

    @website.setter
    def website(self, website):
        self._website = website

    @property
    def landing_page(self):
        """str: Gets and Sets the Landing Page."""
        return self._landing_page

    @landing_page.setter
    def landing_page(self, landing_page):
        self._landing_page = landing_page

    @property
    def type(self):
        """str: Gets and Sets the Type."""
        return self._type

    @type.setter
    def type(self, type):  # type name is by design pylint: disable=redefined-builtin
        self._type = type

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
