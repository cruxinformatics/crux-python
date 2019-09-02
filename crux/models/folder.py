"""Module contains File model."""

from typing import Any, Dict, Union  # noqa: F401

from crux._utils import create_logger, Headers
from crux.models.permission import Permission
from crux.models.resource import Resource


log = create_logger(__name__)


class Folder(Resource):
    """Folder Model."""

    def add_permission(  # It is by design pylint: disable=arguments-differ
        self, identity_id, permission, recursive=False
    ):
        # type: (str, str, bool) -> Union[bool, Permission]
        """Adds permission to the Folder resource.

        Args:
            identity_id (str): Identity Id to be set.
            permission (str): Permission to be set.
            recursive (bool): If recursive is set to True, it will recursive apply
                permission to all resources under the folder resource.

        Returns:
            bool or crux.models.Permission: If recursive is set then it returns True.
                If recursive is unset then it returns Permission object.
        """

        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )

        body = {
            "identityId": identity_id,
            "permission": permission,
            "action": "add",
            "resourceIds": [self.id],
        }
        if recursive:
            log.debug(
                "Adding permission %s for %s in recursive mode to resource %s",
                permission,
                identity_id,
                self.id,
            )
            return self.connection.api_call(
                "POST", ["permissions", "bulk"], headers=headers, json=body
            )
        else:
            log.debug(
                "Adding permission %s for %s to resource %s",
                permission,
                identity_id,
                self.id,
            )
            return self.connection.api_call(
                "PUT",
                ["permissions", self.id, identity_id, permission],
                model=Permission,
                headers=headers,
            )

    def delete_permission(  # It is by design pylint: disable=arguments-differ
        self, identity_id, permission, recursive=False
    ):
        # type: (str, str, bool) -> bool
        """Deletes permission from Folder resource.

        Args:
            identity_id (str): Identity Id for the deletion.
            permission (str): Permission for deletion.
            recursive (bool): If recursive is set to True, it will recursively delete
                permission from all resources under the folder resource.
                Defaults to False.

        Returns:
            bool: True if it is able to delete it.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )

        body = {
            "identityId": identity_id,
            "permission": permission,
            "action": "delete",
            "resourceIds": [self.id],
        }
        if recursive:
            log.debug(
                "Deleting permission %s for %s in recursive mode from resource %s",
                permission,
                identity_id,
                self.id,
            )
            return self.connection.api_call(
                "POST", ["permissions", "bulk"], headers=headers, json=body
            )
        else:
            log.debug(
                "Deleting permission %s for %s in from resource %s",
                permission,
                identity_id,
                self.id,
            )
            return self.connection.api_call(
                "DELETE",
                ["permissions", self.id, identity_id, permission],
                headers=headers,
            )
