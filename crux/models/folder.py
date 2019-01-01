"""Module contains File model."""

from typing import Any, Dict, Union  # noqa: F401 pylint: disable=unused-import

from crux.models.permission import Permission
from crux.models.resource import Resource


class Folder(Resource):
    """Folder Model."""

    @property
    def folder(self):
        """str: Gets and Sets the folder."""
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = folder

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Folder object to Folder Dictionary.

        Returns:
            dict: Folder Dictionary.
        """
        return {
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "folder": self.folder,
            "type": self.type,
            "labels": self.labels,
        }

    def add_permission(  # It is by design pylint: disable=arguments-differ
        self, identity_id="_subscribed_", permission="Read", recursive=False
    ):
        # type: (str, str, bool) -> Union[bool, Permission]
        """Adds permission to the Folder resource.

        Args:
            identity_id (str): Identity Id to be set. Defaults to _subscribed_.
            permission (str): Permission to be set. Defaults to Read.
            recursive (bool): If recursive is set to True, it will recursive apply
                permission to all resources under the folder resource.

        Returns:
            bool or crux.models.Permission: If recursive is set then it returns True.
                If recursive is unset then it returns Permission object.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        params = {
            "identityId": identity_id,
            "permission": permission,
            "action": "add",
            "resourceIds": [self.id],
        }
        if recursive:
            return self.connection.api_call(
                "POST", ["permissions", "bulk"], headers=headers, params=params
            )
        else:
            return self.connection.api_call(
                "PUT",
                ["permissions", self.id, identity_id, permission],
                model=Permission,
                headers=headers,
            )

    def delete_permission(  # It is by design pylint: disable=arguments-differ
        self, identity_id="_subscribed_", permission="Read", recursive=False
    ):
        # type: (str, str, bool) -> bool
        """Deletes permission from Folder resource.

        Args:
            identity_id (str): Identity Id for the deletion. Defaults to _subscribed_.
            permission (str): Permission for deletion. Defaults to Read.
            recursive (bool): If recursive is set to True, it will recursively delete
                permission from all resources under the folder resource.
                Defaults to False.

        Returns:
            bool: True if it is able to delete it.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        params = {
            "identityId": identity_id,
            "permission": permission,
            "action": "delete",
            "resourceIds": [self.id],
        }
        if recursive:
            return self.connection.api_call(
                "POST", ["permissions", "bulk"], headers=headers, params=params
            )
        else:
            return self.connection.api_call(
                "DELETE",
                ["permissions", self.id, identity_id, permission],
                headers=headers,
            )
