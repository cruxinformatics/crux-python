"""Module contains Permission model."""

from crux.models.model import CruxModel


class Permission(CruxModel):
    """Permission Model."""

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
