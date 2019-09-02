"""Module contains Resource model."""

from enum import Enum
import os
import posixpath
from typing import Any, Dict, List, Union  # noqa: F401

from requests.models import Response  # noqa: F401 pylint: disable=unused-import

from crux._utils import create_logger, DEFAULT_CHUNK_SIZE, Headers
from crux.models.model import CruxModel
from crux.models.permission import Permission


log = create_logger(__name__)


class Resource(CruxModel):
    """Resource Model."""

    def __init__(self, object_model=None, connection=None):
        # type: (...) -> None
        """
        Attributes:
            id (str): Resourece Id. Defaults to None.
            dataset_id (str): Dataset Identity. Defaults to None.
            folder_id (str): Folder Identity. Defaults to None.
            folder (str): Folder Name. Defaults to None.
            name (str): Resource name. Defaults to None.
            size (str): Resource size. Defaults to None.
            type (str): Resource type. Defaults to None.
            config (str): Resource config. Defaults to None.
            provenance (list): Resource Provenance. Defaults to None.
            as_of (str): Resource as_of. Defaults to None.
            created_at (str): Resource created_at. Defaults to None.
            modified_at (str): Resource modified_at. Defaults to None.
            storage_id (str): Resource storage Identity. Defaults to None.
            description (str): Resource description. Defaults to None.
            media_type (str): Resource Media Type. Defaults to None.
            tags (:obj:`list` of :obj:`str`): Resource tags. Defaults to None.
            labels (dict): Dictionary containing Label Key and Values.
                Defaults to None.
            connection (crux._client.CruxClient): Connection Object. Defaults to None.
            raw_response (dict): Response Content. Defaults to None.

        Raises:
            ValueError: If name or tags are set to None.
            TypeError: If tags are not of list type.
        """

        self._folder = None
        self.object_model = object_model
        self.connection = connection

    @property
    def id(self):
        """str: Gets the Resource ID."""
        return self.object_model["resourceId"]

    @property
    def description(self):
        """str: Gets the Resource Description."""
        return self.object_model["description"]

    @description.setter
    def description(self, description):
        self.object_model["description"] = description

    @property
    def media_type(self):
        """str: Gets the Resource Description."""
        return self.object_model["mediaType"]

    @property
    def dataset_id(self):
        """str: Gets the Dataset ID."""
        return self.object_model["datasetId"]

    @property
    def folder_id(self):
        """str: Gets the Folder ID."""
        return self.object_model["folderId"]

    @property
    def storage_id(self):
        """str: Gets the Storage ID."""
        return self.object_model["storageId"]

    @property
    def name(self):
        """str: Gets the Resource Name."""
        return self.object_model["name"]

    @name.setter
    def name(self, name):
        self.object_model["name"] = name

    @property
    def config(self):
        """str: Gets the config."""
        return self.object_model["config"]

    @config.setter
    def config(self, config):
        self.object_model["config"] = config

    @property
    def provenance(self):
        """str: Gets the Provenance."""
        return self.object_model["provenance"]

    @provenance.setter
    def provenance(self, provenance):
        self.object_model["provenance"] = provenance

    @property
    def type(self):
        """str: Gets the Resource Type."""
        return self.object_model["type"]

    @property
    def tags(self):
        """:obj:`list` of :obj:`str`: Gets the Resource Tags."""
        return self.object_model["tags"]

    @tags.setter
    def tags(self, tags):
        self.object_model["tags"] = tags

    @property
    def labels(self):
        """dict: Gets the Resource labels."""
        labels = {}
        for label in self.object_model["labels"]:
            labels[label["labelKey"]] = label["labelValue"]
        return labels

    @property
    def as_of(self):
        """str: Gets the as_of."""
        return self.object_model["asOf"]

    @property
    def created_at(self):
        """str: Gets created_at."""
        return self.object_model["createdAt"]

    @property
    def modified_at(self):
        """str: Gets modified_at."""
        return self.object_model["modifiedAt"]

    @property
    def size(self):
        """int: Gets the size."""
        size = self.object_model["size"]
        return int(size if size else 0)

    @property
    def path(self):
        """str: Compute or Get the resource path."""
        return posixpath.join(self.folder, self.name)

    @property
    def folder(self):
        """str: Compute or Get the folder name."""
        if self._folder:
            return self._folder

        self._folder = self._get_folder()
        return self._folder

    @folder.setter
    def folder(self, folder):
        self.object_model["folder"] = folder
        log.debug(self.object_model)
        self._folder = folder

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Resource object to Resource Dictionary.

        Returns:
            dict: Resource Dictionary.
        """
        return self.object_model

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, Any]) -> Any
        """Transforms Resource Dictionary to Resource object.

        Args:
            a_dict (dict): Resource Dictionary.

        Returns:
            crux.models.Resource: Resource Object.
        """

        return cls(object_model=a_dict)

    def delete(self):
        # type: () -> bool
        """Deletes Resource from Dataset.

        Returns:
            bool: True if it is deleted.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        return self.connection.api_call(
            "DELETE", ["resources", self.id], headers=headers
        )

    def update(self, name=None, description=None, tags=None, provenance=None):
        # type: (str, str, List[str], str) -> bool
        """Updates the metadata for Resource.

        Args:
            name (str): Name of resource. Defaults to None.
            description (str): Description of the resource. Defaults to None.
            tags (:obj:`list` of :obj:`str`): List of tags. Defaults to None.
            provenance (str): Provenance for a resource. Defaults to None.

        Returns:
            bool: True, if resource is updated.

        Raises:
            ValueError: It is raised if name, description or tags are unset.
            TypeError: It is raised if tags are not of type List.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        body = {}  # type: Dict[str, Union[str, List, Dict]]

        if name is not None:
            self.object_model["name"] = name
        if description is not None:
            self.object_model["description"] = description
        if tags is not None:
            self.object_model["tags"] = tags
        if provenance is not None:
            self.object_model["provenance"] = provenance

        body = self.to_dict()

        log.debug("Body %s", body)

        resource_object = self.connection.api_call(
            "PUT", ["resources", self.id], headers=headers, json=body, model=Resource
        )

        log.debug(resource_object)

        self.object_model = resource_object.object_model

        log.debug("Updated dataset %s with content %s", self.id, self.object_model)
        return True

    def add_permission(self, identity_id, permission):
        # type: (str, str) -> Union[bool, Permission]
        """Adds permission to the resource.

        Args:
            identity_id: Identity Id to be set.
            permission: Permission to be set.

        Returns:
            crux.models.Permission: Permission Object.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        return self.connection.api_call(
            "PUT",
            ["permissions", self.id, identity_id, permission],
            model=Permission,
            headers=headers,
        )

    def delete_permission(self, identity_id, permission):
        # type: (str, str) -> bool
        """Deletes permission from the resource.

        Args:
            identity_id (str): Identity Id for the deletion.
            permission (str): Permission for the deletion.

        Returns:
            bool: True if it is able to delete it.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        return self.connection.api_call(
            "DELETE", ["permissions", self.id, identity_id, permission], headers=headers
        )

    def list_permissions(self):
        # type: () -> List[Permission]
        """Lists the permission on the resource.

        Returns:
            list (:obj:`crux.models.Permission`): List of Permission Objects.
        """
        headers = Headers({"accept": "application/json"})
        return self.connection.api_call(
            "GET",
            ["resources", self.id, "permissions"],
            model=Permission,
            headers=headers,
        )

    def add_label(self, label_key, label_value):
        # type: (str, str) -> bool
        """Adds label to Resource.

        Args:
            label_key (str): Label Key for Resource.
            label_value (str): Label Value for Resource.

        Returns:
            bool: True if label is added, False otherwise.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        response_result = self.connection.api_call(
            "PUT",
            [
                "datasets",
                self.dataset_id,
                "resources",
                self.id,
                "labels",
                label_key,
                label_value,
            ],
            headers=headers,
        )

        if response_result:
            # Sync the latest data from API to prevent inconsistency
            self.refresh()

        return True

    def delete_label(self, label_key):
        # type: (str) -> bool
        """Deletes label from Resource.

        Args:
            label_key (str): Label Key for Resource.

        Returns:
            bool: True if label is deleted, False otherwise.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        response_result = self.connection.api_call(
            "DELETE",
            ["datasets", self.dataset_id, "resources", self.id, "labels", label_key],
            headers=headers,
        )

        if response_result:
            # Sync the latest data from API to prevent inconsistency
            self.refresh()

        return True

    def add_labels(self, labels_dict):
        # type: (dict) -> bool
        """Adds multiple labels to Resource.

        Args:
            label_dict (dict): Labels (key/value pairs) to add to the Resource.

        Returns:
            bool: True if the labels were added, False otherwise.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )

        labels_list = []
        for label_key, label_value in labels_dict.items():
            if label_key is not None and label_value is not None:
                label_key = (
                    label_key.value if isinstance(label_key, Enum) else label_key
                )
                labels_list.append(
                    {"labelKey": str(label_key), "labelValue": str(label_value)}
                )

        data = {"labels": labels_list}

        response_result = self.connection.api_call(
            "PUT",
            ["datasets", self.dataset_id, "resources", self.id, "labels"],
            headers=headers,
            json=data,
        )

        if response_result:
            # Sync the latest data from API to prevent inconsistency
            self.refresh()

        return True

    def _get_folder(self):
        # type: () -> str
        """Fetches the folder of the resource.

        Returns:
            str: Folder name of the resource.
        """
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        response = self.connection.api_call(
            "GET", ["resources", self.id, "folderpath"], headers=headers
        )

        return response.json().get("path")

    def _download(self, file_obj, media_type, chunk_size=DEFAULT_CHUNK_SIZE):

        if media_type is not None:
            headers = Headers({"accept": media_type})
        else:
            headers = None

        data = self.connection.api_call(
            "GET", ["resources", self.id, "content"], headers=headers, stream=True
        )

        for chunk in data.iter_content(chunk_size=chunk_size):
            file_obj.write(chunk)
        data.close()
        return True

    def refresh(self):
        """Refresh Resource model from API backend.

        Returns:
            bool: True, if it is able to refresh the model,
                False otherwise.
        """
        # type () -> bool
        headers = Headers(
            {"content-type": "application/json", "accept": "application/json"}
        )
        resource_object = self.connection.api_call(
            "GET", ["resources", self.id], headers=headers, model=Resource
        )

        self.object_model = resource_object.object_model

        return True


# https://github.com/python/mypy/issues/2477, mypy is performing checking with Python2
class MediaType(Enum):  # type: ignore
    """MediaType Enumeration Model."""

    JSON = "application/json"
    NDJSON = "application/x-ndjson"
    CSV = "text/csv"
    PARQUET = "application/parquet"
    AVRO = "avro/binary"

    @classmethod
    def detect(cls, file_name):
        # type: (str) -> str
        """Detects the media_type from the file extension.

        Args:
            file_name (str): Absolute or Relative Path of the file.

        Returns:
            str: MediaType extension.

        Raises:
            LookupError: If file type is not supported.
        """
        file_ext = os.path.splitext(file_name)[1][1:].upper()

        if file_ext in cls.__members__:
            return cls[file_ext].value  # type: ignore
        else:
            raise LookupError("File/Media Type not supported.")
