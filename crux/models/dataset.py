"""Module contains Dataset model."""

from collections import defaultdict
from datetime import date, datetime, timedelta
from dateutil import parser
import json
import os
import posixpath
from typing import (
    DefaultDict,
    Dict,
    Generator,
    IO,
    Iterator,
    List,
    MutableMapping,
    Optional,
    Set,
    Text,
    Tuple,
    Union,
)  # noqa: F401

from crux._compat import unicode
from crux._utils import (
    create_logger,
    DELIVERY_ID_REGEX,
    Headers,
    split_posixpath_filename_dirpath,
)
from crux.exceptions import CruxAPIError, CruxClientError, CruxResourceNotFoundError
from crux.models._factory import get_resource_object
from crux.models.delivery import Delivery
from crux.models.file import File
from crux.models.folder import Folder
from crux.models.ingestion import Ingestion
from crux.models.job import StitchJob
from crux.models.label import Label
from crux.models.model import CruxModel
from crux.models.permission import Permission
from crux.models.resource import Resource
from crux.models.resource import MediaType


log = create_logger(__name__)


class Dataset(CruxModel):
    """Dataset Model."""

    @property
    def id(self):
        """str: Gets the Dataset ID."""
        return self.raw_model["datasetId"]

    @property
    def owner_identity_id(self):
        """str: Gets the Owner Identity ID."""
        return self.raw_model.get("ownerIdentityId", "")

    @property
    def contact_identity_id(self):
        """str: Gets the Contact Identity ID."""
        return self.raw_model.get("contactIdentityId", "")

    @property
    def name(self):
        """str: Gets the Dataset Name."""
        return self.raw_model["name"]

    @name.setter
    def name(self, name):
        self.raw_model["name"] = name

    @property
    def tags(self):
        """str: Gets the tags.

        Raises:
            TypeError: If tags is not a list
        """
        return self.raw_model.get("tags", [])

    @tags.setter
    def tags(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Tags should be of type list")
        self.raw_model["tags"] = tags

    @property
    def description(self):
        """str: Gets the Dataset Description."""
        return self.raw_model.get("description", "")

    @description.setter
    def description(self, description):
        self.raw_model["description"] = description

    @property
    def website(self):
        """str: Gets the Dataset Website."""
        return self.raw_model.get("website", "")

    @website.setter
    def website(self, website):
        self.raw_model["website"] = website

    @property
    def created_at(self):
        """str: Gets the Dataset created_at."""
        return self.raw_model.get("createdAt", "")

    @property
    def modified_at(self):
        """str: Gets the Dataset modified_at."""
        return self.raw_model.get("modifiedAt", "")

    @property
    def provenance(self):
        """str: Compute or Get the provenance."""
        return self.raw_model.get("provenance", "")

    def create(self):
        # type: () -> bool
        """Creates the Dataset.

        Returns:
            bool: True if dataset is created.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        dataset_object = self.connection.api_call(
            "POST", ["datasets"], json=self.raw_model, model=Dataset, headers=headers
        )

        self.raw_model = dataset_object.raw_model

        return True

    def delete(self):
        # type: () -> bool
        """Deletes the Dataset.

        Returns:
            bool: True if dataset is deleted.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call("DELETE", ["datasets", self.id], headers=headers)

    def update(self, name=None, description=None, tags=None):
        # type: (str, str, List[str]) -> bool
        """Updates the Dataset.

        Args:
            name (str): Name of the dataset. Defaults to None.
            description (str): Description of the dataset. Defaults to None.
            tags (:obj:`list` of :obj:`str`): List of tags. Defaults to None.

        Returns:
            bool: True, if dataset is updated.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        if name is not None:
            self.raw_model["name"] = name
        if description is not None:
            self.raw_model["description"] = description
        if tags is not None:
            self.raw_model["tags"] = tags

        body = self.raw_model

        dataset_object = self.connection.api_call(
            "PUT", ["datasets", self.id], headers=headers, json=body, model=Dataset
        )

        self.raw_model = dataset_object.raw_model

        log.debug("Updated dataset %s with content %s", self.id, dataset_object.__dict__)
        return True

    def refresh(self):
        """Refresh Resource model from API backend.

        Returns:
            bool: True, if it is able to refresh the model,
                False otherwise.
        """
        # type () -> bool
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        dataset_object = self.connection.api_call(
            "GET", ["datasets", self.id], headers=headers, model=Resource
        )

        self.raw_model = dataset_object.raw_model

        return True

    def create_file(self, path, tags=None, description=None):
        # type: (str, List[str], str) -> File
        """Creates File resource in Dataset.

        Args:
            path (str): Path of the file resource.
            tags (:obj:`list` of :obj:`str`): Tags of the file resource.
                Defaults to None.
            description (str): Description of the file resource.

        Returns:
            crux.models.File: File Object.
        """

        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        tags = tags if tags else []

        file_name, folder = split_posixpath_filename_dirpath(path)

        raw_model = {
            "name": file_name,
            "type": "file",
            "tags": tags,
            "description": description,
            "folder": folder,
        }

        file_resource = File(raw_model=raw_model)

        return self.connection.api_call(
            "POST",
            ["datasets", self.id, "resources"],
            json=file_resource.raw_model,
            model=File,
            headers=headers,
        )

    def create_folder(self, path, folder="/", tags=None, description=None):
        # type: (str, str, List[str], str) -> Folder
        """Creates Folder resource in Dataset.

        Args:
            path (str): Path of the Folder resource.
            folder (str): Parent folder of the Folder resource.
                Defaults to /.
            tags (:obj:`list` of :obj:`str`): Tags of the Folder resource.
                Defaults to None.
            description (str): Description of the Folder resource.
                Defaults to None.

        Returns:
            crux.models.Folder: Folder Object.
        """

        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        tags = tags if tags else []

        file_name, folder = split_posixpath_filename_dirpath(path)

        raw_model = {
            "name": file_name,
            "type": "folder",
            "tags": tags,
            "description": description,
            "folder": folder,
        }

        folder_resource = Folder(raw_model=raw_model)

        return self.connection.api_call(
            "POST",
            ["datasets", self.id, "resources"],
            json=folder_resource.raw_model,
            model=Folder,
            headers=headers,
        )

    def _get_resource(self, path, model):
        """Gets the resource object from the string path.

        Args:
            path (str): Resource path.
            crux.models.Resource: Resource model.

        Returns:
            crux.models.Resource: Resource model Object.

        Raises:
            crux.exceptions.CruxResourceNotFoundError: If resource is not found.
        """
        resource_name, folder_path = split_posixpath_filename_dirpath(path)
        resource_gen = self._list_resources(
            folder=folder_path, limit=1, name=resource_name, include_folders=True, model=model,
        )
        try:
            return next(resource_gen)
        except StopIteration as ex:
            log.debug("Parse exception: %s" % str(ex))
            # As of now API can't fetch id from the resource path or name,
            # hence raising the 404 error from the Python client
            raise CruxResourceNotFoundError({"statusCode": 404, "name": resource_name})

    def _resource_exists(self, path):
        # type: (str) -> bool
        """Checks the existence of resource.

        Args:
            path (str): Resource Path.

        Returns:
            bool: True if resource exists.

        Raises:
            crux.exceptions.CruxResourceNotFoundError: If resource is not found.
        """
        try:
            self._get_resource(path=path, model=Resource)
            return True
        except CruxResourceNotFoundError:
            return False

    def get_file(self, path):
        # type: (str) -> File
        """Gets the File resource object.

        Args:
            path (str): File resource path.

        Returns:
            crux.models.File: File Object.
        """
        return self._get_resource(path=path, model=File)

    def get_folder(self, path):
        # type: (str) -> Folder
        """Gets the Folder resource object.

        Args:
            path (str): Folder resource path.

        Returns:
            crux.models.Folder: Folder Object.
        """
        return self._get_resource(path=path, model=Folder)

    def list_resources(
        self, folder="/", cursor=None, limit=1, include_folders=False, sort=None
    ):
        # type: (str, str, int, bool, str) -> Generator[Resource]
        """Lists the resources in Dataset.

        Args:
            folder (str): Folder for which resource should be listed.
                Defaults to /.
            cursor (str): Sets the offset to the page cursor. Defaults to None.
            limit (int): Sets the limit. Defaults to 1.
            include_folders (bool): Sets whether to include folders or not.
                Defaults to False.
            sort (str): Sets whether to sort or not.
                Defaults to None.

        Returns:
            list (:obj:`crux.models.Resource`): List of File resource objects.
        """
        result_gen = self._list_resources(
            sort=sort,
            folder=folder,
            cursor=cursor,
            limit=limit,
            include_folders=include_folders,
            model=Resource,
        )

        for result in result_gen:
            yield result

    def download_files(self, folder, local_path, only_use_crux_domains=None):
        # type: (str, str, bool) -> List[str]
        """Downloads the resources recursively.

        Args:
            folder (str): Crux Dataset Folder from where the
                file resources should be recursively downloaded.
            local_path (str): Local OS Path where the file resources should be downloaded.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Returns:
            list (:obj:`str`): List of location of download files.

        Raises:
            ValueError: If Folder or local_path is None.
            OSError: If local_path is an invalid directory location.
        """
        if folder is None:
            raise ValueError("Folder value shouldn't be empty")

        if local_path is None:
            raise ValueError("Local Path value shouldn't be empty")

        if not os.path.exists(local_path) and not os.path.isdir(local_path):
            raise OSError("local_path is an invalid directory location")

        resources_gen = self._list_resources(
            sort=None,
            folder=folder,
            cursor=None,
            limit=None,
            include_folders=True,
            model=Resource,
        )

        for resource in resources_gen:
            resource_path = posixpath.join(folder, resource.name)
            resource_local_path = os.path.join(local_path, resource.name)
            if resource.type == "folder":
                if not os.path.exists(resource_local_path):
                    os.mkdir(resource_local_path)
                log.debug("Created local directory %s", resource_local_path)
                result_gen = self.download_files(
                    folder=resource_path,
                    local_path=resource_local_path,
                    only_use_crux_domains=only_use_crux_domains,
                )
                for result in result_gen:
                    yield result
            elif resource.type == "file":
                file_resource = File.from_dict(resource.to_dict(), connection=self.connection)
                file_resource.download(
                    resource_local_path, only_use_crux_domains=only_use_crux_domains
                )
                yield resource_local_path
                log.debug("Downloaded file at %s", resource_local_path)

    def upload_files(
        self,
        local_path,
        folder,
        media_type=None,
        description=None,
        tags=None,
        only_use_crux_domains=None,
    ):
        # type: (str, str, str, str, List[str], bool) -> List[File]
        """Uploads the resources recursively.

        Args:
            local_path (str): Local OS Path from where the file resources should be uploaded.
            media_type (str): Content Types of File resources to be uploaded.
                Defaults to None.
            folder (str): Crux Dataset Folder where file resources
                should be recursively uploaded.
            description (str): Description to be set on uploaded resources.
                Defaults to None.
            tags (:obj:`list` of :obj:`str`): Tags to be set on uploaded resources.
                Defaults to None.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Returns:
            list (:obj:`crux.models.File`): List of uploaded file objects.

        Raises:
            ValueError: If folder or local_path is None.
            OSError: If local_path is an invalid directory location.
        """
        tags = tags if tags else []

        uploaded_file_objects = []  # type: List[File]

        if folder is None:
            raise ValueError("Folder value shouldn't be empty")

        if local_path is None:
            raise ValueError("Local Path value shouldn't be empty")

        if not os.path.exists(local_path) and not os.path.isdir(local_path):
            raise OSError("local_path is an invalid directory location")

        for content in os.listdir(local_path):
            content_local_path = os.path.join(local_path, content)
            content_path = posixpath.join(folder, content)
            if os.path.isdir(content_local_path):
                self.create_folder(path=content_path, tags=tags, description=description)
                log.debug("Created folder %s in dataset %s", content_path, self.id)
                uploaded_file_objects += self.upload_files(
                    media_type=media_type,
                    folder=content_path,
                    local_path=content_local_path,
                    tags=tags,
                    description=description,
                    only_use_crux_domains=only_use_crux_domains,
                )

            elif os.path.isfile(content_local_path):
                fil_o = self.upload_file(
                    content_local_path,
                    content_path,
                    media_type=media_type,
                    tags=tags,
                    description=description,
                    only_use_crux_domains=only_use_crux_domains,
                )
                uploaded_file_objects.append(fil_o)
                log.debug("Uploaded file %s in dataset %s", content_path, self.id)

        return uploaded_file_objects

    def list_files(self, sort=None, folder="/", cursor=None, limit=100):
        # type: (str, str, str, int) -> List[File]
        """Lists the files.

        Args:
            sort (str): Sets whether to sort or not. Defaults to None.
            folder (str): Folder for which resource should be listed.
                Defaults to /.
            cursor (str): Sets the offset to the page cursor. Defaults to None.
            limit (int): Sets the limit. Defaults to 100.

        Returns:
            list (:obj:`crux.models.File`): List of File objects.
        """
        resource_list_gen = self._list_resources(
            sort=sort,
            folder=folder,
            cursor=cursor,
            limit=limit,
            include_folders=False,
            model=File,
        )

        for resource in resource_list_gen:
            if resource.type == "file":
                yield resource

    def _list_resources(
        self,
        folder="/",
        cursor=None,
        limit=1,
        include_folders=False,
        name=None,
        model=None,
        sort=None,
    ):

        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        params = {"datasetId": self.id, "folder": folder}

        if cursor:
            params["cursor"] = cursor

        if sort:
            params["sort"] = sort

        if name:
            params["name"] = name

        if include_folders:
            params["includeFolders"] = "true"
        else:
            params["includeFolders"] = "false"

        retrieved = 0
        pagesize = 500
        paginate = {}
        while limit is None or retrieved < limit:
            params["limit"] = None if limit is None else min(pagesize, limit - retrieved)

            resp = self.connection.api_call(
                "GET",
                ["resources"],
                params=params,
                model=model,
                headers=headers,
                paginate=paginate,
            )
            resp_count = len(resp)

            if resp_count == 0:
                break

            for resource in resp:
                yield resource

            retrieved += resp_count
            params["cursor"] = paginate["cursor"]

    def upload_file(
        self,
        src,
        dest,
        media_type=None,
        description=None,
        tags=None,
        only_use_crux_domains=None,
    ):
        # type: (Union[IO, str], str, str, str, List[str], bool) -> File
        """Uploads the File.

        Args:
            src (str or file): Local OS path whose content
                is to be uploaded to file resource.
            dest (str): File resource path.
            media_type (str): Content type of the file. Defaults to None.
            description (str): Description of the file. Defaults to None.
            tags (:obj:`list` of :obj:`str`): Tags to be attached to the file resource.
            only_use_crux_domains (bool): True if content is required to be downloaded
                from Crux domains else False.

        Returns:
            crux.models.File: File Object.
        """
        tags = tags if tags else []

        file_resource = self.create_file(tags=tags, description=description, path=dest)

        try:
            return file_resource.upload(
                src, media_type=media_type, only_use_crux_domains=only_use_crux_domains
            )
        except (CruxClientError, CruxAPIError, IOError):
            file_resource.delete()
            raise

    def add_permission_to_resources(
        self,
        identity_id,
        permission,
        resource_paths=None,
        resource_objects=None,
        resource_ids=None,
    ):
        # type: (str, str, List[str], List[Union[File,Folder]], List[str]) -> bool
        """Adds permission to all or specific Dataset resources.

        Args:
            identity_id (str): Identity Id to be set.
            permission (str): Permission to be set.
            resource_paths (:obj:`list` of :obj:`str`): List of resource paths on which the
                permission should be applied. If none of resource_paths,
                resource_objects or resource_ids parameter is set,
                then it will apply the permission to whole dataset.
            resource_objects (:obj:`list` of :obj:`crux.models.Resource`): List of
                resource objects on which the permission should be applied.
                Overrides resource_paths.
                If none of resource_paths, resource_objects or
                resource_ids parameter is set, then it will apply the
                permission to whole dataset.
            resource_ids (:obj:`list` of :obj:`str`): List of resource ids on which
                permission should be applied. Overrides resource_pathss and resource_objects.
                If none of resource_paths,
                resource_objects or resource_ids parameter is set,
                then it will apply the permission to whole dataset.

        Returns:
            bool: True if permission is applied.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        body = {
            "identityId": identity_id,
            "permission": permission,
            "action": "add",
        }  # type: Dict[str, Union[str, List[str]]]

        if resource_ids or resource_objects or resource_paths:
            if resource_paths:
                log.debug(
                    "Add permission %s to %s for resource paths", permission, identity_id,
                )
                resource_ids = list()
                for resource_path in resource_paths:
                    resource_object = self._get_resource(path=resource_path, model=Resource)
                    resource_ids.append(resource_object.id)
                body["resourceIds"] = resource_ids

            if resource_objects:
                log.debug(
                    "Add permissions %s to %s for resource objects", permission, identity_id,
                )
                resource_ids = list()
                for resource_object in resource_objects:
                    resource_ids.append(resource_object.id)
                body["resourceIds"] = resource_ids

            if resource_ids:
                log.debug("Add permissions %s to %s for resource ids", permission, identity_id)
                body["resourceIds"] = resource_ids
        else:
            log.debug(
                "Add permission %s to %s for dataset %s", permission, identity_id, self.id,
            )
            body["datasetId"] = self.id

        return self.connection.api_call(
            "POST", ["permissions", "bulk"], headers=headers, json=body
        )

    def delete_permission_from_resources(
        self,
        identity_id,
        permission,
        resource_paths=None,
        resource_objects=None,
        resource_ids=None,
    ):
        # type: (str, str, List[str], List[Union[File,Folder]], List[str]) -> bool
        """Method which deletes permission from all or specific Dataset resources.

        Args:
            identity_id (str): Identity Id for the deletion.
            permission (str): Permission for the deletion.
            resource_paths (:obj:`list` of :obj:`crux.models.Resource`): List of
                resource path from which the permission should be deleted.
                If none of resource_paths,
                resource_objects or resource_ids parameter is set,
                then it will delete the permission from whole dataset.
            resource_objects (:obj:`list` of :obj:`crux.models.Resource`): List of
                resource objects from which the permission should be deleted.
                Overrides resource_paths.
                If none of resource_paths, resource_objects or resource_ids parameter is
                set, then it will delete the permission from whole dataset.
            resource_ids (:obj:`list` of :obj:`crux.models.Resource`): List of
                resource ids from which the permission should be deleted.
                Overrides resource_paths and resource_objects.
                If none of resource_paths, resource_objects or
                resource_ids parameter is set, then it will delete the
                permission from whole dataset.

        Returns:
            bool: True if it is able to delete the permission.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        body = {
            "identityId": identity_id,
            "permission": permission,
            "action": "delete",
        }  # type: Dict[str, Union[str, List[str]]]

        if resource_ids or resource_objects or resource_paths:
            if resource_paths:
                log.debug(
                    "Delete permission %s for %s from resource paths", permission, identity_id,
                )
                resource_ids = list()
                for resource_path in resource_paths:
                    resource_object = self._get_resource(path=resource_path, model=Resource)
                    resource_ids.append(resource_object.id)
                body["resourceIds"] = resource_ids

            if resource_objects:
                log.debug(
                    "Delete permission %s for %s from resource objects",
                    permission,
                    identity_id,
                )
                resource_ids = list()
                for resource_object in resource_objects:
                    resource_ids.append(resource_object.id)
                body["resourceIds"] = resource_ids

            if resource_ids:
                log.debug(
                    "Delete permission %s for %s from resource ids", permission, identity_id,
                )
                body["resourceIds"] = resource_ids
        else:
            log.debug(
                "Delete permission %s for %s from dataset %s",
                permission,
                identity_id,
                self.id,
            )
            body["datasetId"] = self.id

        return self.connection.api_call(
            "POST", ["permissions", "bulk"], headers=headers, json=body
        )

    def add_permission(self, identity_id, permission):
        # type: (str, str) -> Union[bool, Permission]
        """Adds permission to the Dataset.

        Args:
            identity_id: Identity Id to be set.
            permission: Permission to be set.

        Returns:
            crux.models.Permission: Permission Object.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }  # type: MutableMapping[Text, Text]
        return self.connection.api_call(
            "PUT",
            ["permissions", self.id, identity_id, permission],
            model=Permission,
            headers=headers,
        )

    def delete_permission(self, identity_id, permission):
        # type: (str, str) -> bool
        """Deletes permission from the Dataset.

        Args:
            identity_id (str): Identity Id for the deletion.
            permission (str): Permission for the deletion.

        Returns:
            bool: True if it is able to delete it.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }  # type: MutableMapping[Text, Text]
        return self.connection.api_call(
            "DELETE", ["permissions", self.id, identity_id, permission], headers=headers
        )

    def list_permissions(self):
        # type: () -> List[Permission]
        """Lists the permission on the Dataset.

        Returns:
            list (:obj:`crux.models.Permission`): List of Permission Objects.
        """
        headers = {"Accept": "application/json"}  # type: MutableMapping[Text, Text]
        return self.connection.api_call(
            "GET", ["datasets", self.id, "permissions"], model=Permission, headers=headers,
        )

    def add_label(self, label_key, label_value):
        # type: (str, str) -> bool
        """Adds label to Dataset.

        Args:
            label_key (str): Label Key for Dataset.
            label_value (str): Label Value for Dataset.

        Returns:
            bool: True if labels are added.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call(
            "PUT", ["datasets", self.id, "labels", label_key, label_value], headers=headers,
        )

    def delete_label(self, label_key):
        # type: (str) -> bool
        """Deletes label from Dataset.

        Args:
            label_key (str): Label Key for Dataset.

        Returns:
            bool: True if labels are deleted.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call(
            "DELETE", ["datasets", self.id, "labels", label_key], headers=headers
        )

    def get_label(self, label_key):
        # type: (str) -> Label
        """Gets label value of Dataset.

        Args:
            label_key (str): Label Key for Dataset.

        Returns:
            crux.models.Label: Label Object.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call(
            "GET", ["datasets", self.id, "labels", label_key], headers=headers, model=Label,
        )

    def find_resources_by_label(self, predicates, max_per_page=1000):
        # type: (List[Dict[str,str]],int)->Iterator[Union[File,Folder]]
        """Method which searches the resouces for given labels in Dataset

        Each predicate can be either:

        - Lexicographical equal
        - Lexicographical less than
        - Lexicographical less than or equal to
        - Lexicographical greater than
        - Lexicographical greater than or equal to
        - A list of OR predicates
        - A list of AND predicates

        .. code-block:: python

            predicates = [
                {"op": "eq", "key": "key1", "val": "abcd"},
                {"op": "ne", "key": "key1", "val": "zzzz"},
                {"op": "lt", "key": "key1", "val": "abd"},
                {"op": "gt", "key": "key1", "val": "abc"},
                {"op": "lte", "key": "key1", "val": "abd"},
                {"op": "gte", "key": "key1", "val": "abc"},
                {"op": "or", "in":
                    [
                        {"op": "eq", "key": "key1", "val": "abcd"},
                        # more OR predicates...
                    ]
                },
                {"op": "and", "in":
                    [
                        {"op": "eq", "key": "key1", "val": "abcd"},
                        # more AND predicates...
                    ]
                }
            ]

        Args:
            predicates (:obj:`list` of :obj:`dict`): List of dictionary predicates
                for finding resources.
            max_per_page (int): Pagination limit. Defaults to 1000.

        Returns:
            list (:obj:`crux.models.Resource`): List of resource matching the query parameters.

        Example:
            .. code-block:: python

                from crux import Crux

                conn = Crux()
                dataset_object = conn.get_dataset(id="dataset_id")
                predicates=[
                    {"op":"eq","key":"test_label1","val":"test_value1"}
                ]
                resource_objects = dataset_object.find_resources_by_label(
                    predicates=predicates
                )
        """

        predicates = predicates if predicates else []

        query_params = {"limit": max_per_page}

        predicates_query = {"basic_query": predicates}  # type: Dict[str, List[Dict[str,str]]]

        after = None
        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        while True:

            if after:
                query_params["after"] = after

            response = self.connection.api_call(
                "POST",
                ["datasets", self.id, "labels", "search"],
                headers=headers,
                json=predicates_query,
                params=query_params,
            )

            resource_list = response.json().get("results")
            if resource_list:
                after = resource_list[-1].get("resourceId")
                for resource in resource_list:
                    obj = get_resource_object(
                        resource_type=resource.get("type"),
                        data=resource,
                        connection=self.connection,
                    )
                    yield obj
            else:
                return

    def stitch(
        self, source_resources, destination_resource, labels=None, tags=None, description=None,
    ):
        # type: (List[Union[str, File]], str, str, List[str], str) -> Tuple[File, str]
        """Method which stitches multiple Avro resources into single Avro resource

        Args:
            source_resources (:obj:`list` of :obj:`str` or :obj:`file`): List of resource paths
                which are to be stitched.
            destination_resource (str): Resource Path to load the stitched output
            labels (dict): Key/Value labels that should be applied to stitched resource
            tags (:obj:`list` of :obj:`str`): List of tags to be applied
                on destination resource.
                Taken into consideration if resource is required to be created.
            description (str): Description to be applied created destination.
                Taken into consideration if resource is required to be created.

        Returns:
            tuple (:obj:`crux.models.File`, :obj:`str`): File object of destination resource.
                    Job ID for background running job.
        Raises:
            TypeError: Source and Destination resource should be of type File or String
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        source_resource_ids = list()
        for resource in source_resources:
            if isinstance(resource, File):
                log.debug("Stitch source resources are of type crux.models.File")
                source_resource_ids.append(resource.id)
            elif isinstance(resource, (str, unicode)):
                log.debug("Stitch source resources are of type string")
                resource_object = self._get_resource(path=resource, model=File)
                source_resource_ids.append(resource_object.id)
            else:
                raise TypeError(
                    "Invalid Type. It should be File resource object or path string"
                )

        if isinstance(destination_resource, File):
            log.debug("Stitch destination resource is of type crux.models.File")
            destination_file_object = destination_resource
        elif isinstance(destination_resource, str):
            log.debug("Stitch destination resource is of type string")
            if self._resource_exists(path=destination_resource):
                destination_file_object = self._get_resource(
                    path=destination_resource, model=File
                )
            else:
                log.debug("Creating file resource at %s", destination_resource)
                destination_file_object = self.create_file(
                    path=destination_resource,
                    description=description,
                    tags=tags if tags else [],
                )
        else:
            raise TypeError("Invalid Type. It should be File resource object or path string")

        data = {
            "sourceResourceIds": source_resource_ids,
            "destinationResourceId": destination_file_object.id,
            "labelsToApply": labels if labels else {},
        }
        response = self.connection.api_call(
            "POST", ["datasets", self.id, "stitch"], headers=headers, json=data
        )

        raw_json = response.json().get("destinationResource")

        file_object = Resource.from_dict(raw_json, connection=self.connection)

        job_id = response.json().get("jobId")

        return (file_object, job_id)

    def get_stitch_job(self, job_id):
        # type: (str) -> StitchJob
        """Stitch Job Details.

        Args:
            job_id (str): Job ID of the Stitch Job.

        Returns:
            crux.models.StitchJob: StitchJob object.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call(
            "GET", ["datasets", "stitch", job_id], headers=headers, model=StitchJob
        )

    def get_delivery(self, delivery_id):
        # type: (str) -> Delivery
        """Gets Delivery object.

        Args:
            delivery_id (str): Delivery ID.

        Returns:
            crux.models.Delivery: Delivery Object.
        Raises:
            ValueError: If delivery_id value is invalid.
        """
        headers = Headers({"accept": "application/json"})

        if not DELIVERY_ID_REGEX.match(delivery_id):
            raise ValueError("Value of delivery_id is invalid")

        return self.connection.api_call(
            "GET", ["deliveries", self.id, delivery_id], headers=headers, model=Delivery
        )

    def get_ingestions(
        self, start_date=None, end_date=None, delivery_status=None, use_cache=None
    ):
        # type: (str, str, str, bool) -> Iterator[Ingestion]
        """Gets Ingestions.

        Args:
            start_date (str): ISO format start time.
            end_date (str): ISO format end time.
            delivery_status (str): Delivery status enum
            use_cache (bool): Preference to set cached response

        Returns:
            crux.models.Delivery: Delivery Object.
        """
        headers = Headers({"accept": "application/json"})

        params = {}
        params["start_date"] = start_date
        params["end_date"] = end_date

        if delivery_status:
            params["delivery_status"] = delivery_status.upper()

        if use_cache is not None:
            params["useCache"] = use_cache

        response = self.connection.api_call(
            "GET", ["deliveries", self.id, "ids"], headers=headers, params=params
        )

        response_json = response.json()
        if isinstance(response_json, dict):
            all_deliveries = response_json.get("delivery_ids")
        else:
            all_deliveries = response_json

        ingestion_set = defaultdict(set)  # type: DefaultDict[str, Set]

        for delivery in all_deliveries:
            if not DELIVERY_ID_REGEX.match(delivery):
                raise ValueError("Value of delivery_id is invalid")
            ingestion_id, version_id = delivery.split(".")
            ingestion_set[ingestion_id].add(int(version_id))

        for ingestion_id in ingestion_set:
            obj = Ingestion.from_dict(
                {
                    "ingestionId": ingestion_id,
                    "versions": ingestion_set[ingestion_id],
                    "datasetId": self.id,
                }
            )
            obj.connection = self.connection
            yield obj

    def get_latest_files(
        self,
        frames=None,
        file_format=MediaType.AVRO.value,
        cutoff_date=None,
        dayfirst=False,
        yearfirst=False,
        delivery_status=None,
        use_cache=None,
    ):
        # type: (Optional[Union[str, List]], str, str, bool, bool, str, bool) -> Iterator[File]
        """Get the latest dataset file resources. The latest supplier_implied_dt with the
        best single delivery version for each frame is selected.

        Args:
            frames (str, list): filter for selected frames
            file_format (str): File format of delivery
            cutoff_date (datetime, str): Search up to this date
            dayfirst (str): Parse format for str date
            yearfirst (str): Parse format for str date
            delivery_status (str): Delivery status enum
            use_cache (bool): Preference to set cached response

        Returns:
            list (:obj:`crux.models.File`): List of file resources.
        """

        if isinstance(frames, list):
            frames = set([x.upper() for x in frames])
        elif isinstance(frames, str):
            frames = {frames.upper()}
        elif frames is not None:
            raise ValueError("Value of frames is invalid")
        if cutoff_date is None:
            now = datetime.utcnow()
            codt = datetime(year=now.year, month=now.month, day=now.day)
        elif isinstance(cutoff_date, datetime):
            codt = datetime(
                year=cutoff_date.year, month=cutoff_date.month, day=cutoff_date.day
            )
        elif isinstance(cutoff_date, str):
            try:
                codt = parser.parse(cutoff_date, dayfirst=dayfirst, yearfirst=yearfirst)
                codt = datetime(year=codt.year, month=codt.month, day=codt.day)
            except:
                raise ValueError("Value of start_date is invalid")
        else:
            raise ValueError("start_date must be str or datetime")

        # look back a couple extra days in case query is performed over the weekend
        lookbacks = [
            {
                "start": codt - timedelta(days=3),
                "end": None if cutoff_date is None else codt,
            },
            {
                "start": codt - timedelta(days=16),
                "end": codt - timedelta(days=4),
            },
            {
                "start": codt - timedelta(days=32),
                "end": codt - timedelta(days=17),
            },
            {
                "start": codt - timedelta(days=92),
                "end": codt - timedelta(days=33),
            },
            {
                "start": codt - timedelta(days=212),
                "end": codt - timedelta(days=93),
            },
            {
                "start": codt - timedelta(days=366),
                "end": codt - timedelta(days=213),
            },
        ]

        found_frames = set()
        found_files = []
        for dt in lookbacks:
            series = self.get_files_range(
                start_date=dt["start"],
                end_date=dt["end"],
                file_format=file_format,
                latest_only=True,
                delivery_status=delivery_status,
                use_cache=use_cache,
            )
            for item in series:
                frame_id = item.frame_id.upper()
                found_frames.add(frame_id)
                if frames and frame_id not in frames:
                    continue
                found_files.append(item)

            if found_frames:
                break
        if frames is not None and found_frames and not found_frames.issuperset(frames):
            unused_frames = found_frames - frames
            log.info(f"One or more specified frames not found. Unused frames: %s", unused_frames)
        return found_files

    def get_files_range(
        self,
        start_date,  # type: Union[datetime, str]
        end_date=None,  # type: Optional[Union[datetime, str]]
        frames=None,  # type: Optional[Union[str, list]]
        file_format=MediaType.AVRO.value,  # type: str
        dayfirst=False,  # type: bool
        yearfirst=False,  # type: bool
        latest_only=False,  # type: bool
        delivery_status=None,  # type: str
        use_cache=None,  # type: bool
    ):
        # type: (...) -> Iterator[File]
        """Get a set of dataset file resources. The best single delivery version for each
        supplier_implied_dt is selected for the given time range.

        Args:
            start_date (str): ISO format start datetime or any paresable date string
            end_date (str): ISO format end datetime or any parseable date string
            delivery_status (str): Delivery status enum
            frames (str, list): filter for selected frames
            file_format (str): File format of delivery
            dayfirst (str): Parse format for str date
            yearfirst (str): Parse format for str date
            latest_only (bool): Return latest files only
            delivery_status (str): Delivery status enum
            use_cache (bool): Preference to set cached response

        Returns:
            list (:obj:`crux.models.File`): List of file resources.
        """

        if isinstance(frames, list):
            frames = set([x.upper() for x in frames])
        elif isinstance(frames, str):
            frames = {frames.upper()}
        elif frames is not None:
            raise ValueError("Value of frames is invalid")

        if isinstance(file_format, MediaType):
            file_format = file_format.value
        else:
            if file_format not in [item.value for item in MediaType]:
                raise ValueError("Value of file_format is invalid")

        fullday = timedelta(minutes=23 * 60 + 59)
        if isinstance(start_date, datetime):
            stdt = start_date.date()
        elif isinstance(start_date, str):
            try:
                stdt = parser.parse(start_date, dayfirst=dayfirst, yearfirst=yearfirst)
            except:
                raise ValueError("Value of start_date is invalid")
        else:
            raise ValueError("start_date must be str or datetime")
        stdt = datetime(year=stdt.year, month=stdt.month, day=stdt.day)

        if end_date is None:
            enddt = None
        elif isinstance(end_date, datetime):
            enddt = end_date.date()
        elif isinstance(end_date, str):
            try:
                enddt = parser.parse(end_date, dayfirst=dayfirst, yearfirst=yearfirst)
            except:
                raise ValueError("Value of end_date is invalid")
        else:
            raise ValueError("date must be str or datetime")
        enddt = None if enddt is None else datetime(year=enddt.year, month=enddt.month, day=enddt.day) + fullday

        headers = Headers({"accept": "application/json"})
        delivery_status = "DELIVERY_SUCCEEDED" if delivery_status is None else delivery_status
        use_cache = True if use_cache is None else use_cache
        params = {
            "start_date": stdt,
            "end_date": None if enddt is None else enddt + timedelta(days=3),
            "delivery_status": delivery_status,
            "use_cache": use_cache,
        }
        response = self.connection.api_call(
            "GET", ["deliveries", self.id, "ids"], headers=headers, params=params
        )
        response_json = response.json()
        if isinstance(response_json, dict):
            all_deliveries = response_json.get("delivery_ids")
        else:
            all_deliveries = response_json

        frame_resources = {}
        resource_delivery_ids = {}
        select_deliveries = all_deliveries[-20:] if latest_only else all_deliveries
        for delivery_id in select_deliveries:
            if not DELIVERY_ID_REGEX.match(delivery_id):
                raise ValueError("Value of delivery_id is invalid")
            params = {"delivery_resource_format": file_format}
            response = self.connection.api_call(
                "GET", ["deliveries", self.id, delivery_id, "data"], params=params
            )
            data = response.json()
            for item in data["resources"]:
                frame_id = item["frame_id"].upper()
                resource_id = item["resource_id"]
                if frame_id not in frame_resources:
                    frame_resources[frame_id] = {
                        "resource_ids": [],
                        "best_deliveries": {},
                    }
                frame_resources[frame_id]["resource_ids"].append(resource_id)
                resource_delivery_ids[resource_id] = delivery_id

        found_frames = set(frame_resources)
        if frames is None:
            process_frames = found_frames
        else:
            process_frames = frames.intersection(found_frames)
            if found_frames and not found_frames.issuperset(frames):
                unused_frames = found_frames - frames
                log.info("One or more specified frames not found. Unused frames: %s", unused_frames)
        resource_ids = [i for s in process_frames for i in frame_resources[s]["resource_ids"]]
        for file in self.get_resources_batch(resource_ids):
            frame_id = file.frame_id.upper()
            dt = (
                file.supplier_implied_dt
                if file.supplier_implied_dt is not None
                else file.ingestion_time
            )
            if dt < stdt.isoformat() or (enddt is not None and dt > enddt.isoformat()):
                continue
            best_deliveries = frame_resources[frame_id]["best_deliveries"]
            if (
                dt not in best_deliveries
                or file.ingestion_time > best_deliveries[dt].ingestion_time
                or (
                    file.ingestion_time == best_deliveries[dt].ingestion_time
                    and resource_delivery_ids[file.id]
                    > resource_delivery_ids[best_deliveries[dt].id]
                )
            ):
                best_deliveries[dt] = file

        for frame_id in process_frames:
            best_deliveries = frame_resources[frame_id]["best_deliveries"]
            for cnt, dt in enumerate(sorted(best_deliveries), 1):
                if latest_only and cnt != len(best_deliveries):
                    continue
                yield best_deliveries[dt]

    def get_resources_batch(self, resource_ids):
        # type: (list) -> Iterator[File]
        """Gets resource metadata.

        Args:
            resource_ids (list): List of resource IDs

        Returns:
            list (:obj:`crux.models.File`): List of file resources.
        """
        headers = Headers({"accept": "application/json"})
        limit = 250
        for i in range(0, len(resource_ids), limit):
            chunk = resource_ids[i : i + limit]
            response = self.connection.api_call(
                "POST",
                ["resources", "get-batch"],
                params={"limit": limit + 1},
                headers=headers,
                data=json.dumps(chunk),
            )
            for resource in response.json():
                obj = File(raw_model=resource)
                obj.connection = self.connection
                yield obj
