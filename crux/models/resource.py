"""Module contains Resource model."""

from enum import Enum
import os
import posixpath
from typing import Dict, List, Union  # noqa: F401

from requests.models import Response  # noqa: F401 pylint: disable=unused-import

from crux._client import CruxClient
from crux._utils import create_logger, DEFAULT_CHUNK_SIZE, Headers
from crux.models.model import CruxModel
from crux.models.permission import Permission


log = create_logger(__name__)


class Resource(CruxModel):
    """Resource Model."""

    def __init__(self, raw_model=None, connection=None):
        # type: (Dict, CruxClient) -> None
        """
        Attributes:
            raw_model (dict): Resource raw dictionary. Defaults to None.
            connection (CruxClient): Connection Object. Defaults to None.
        """
        self._folder = None
        super(Resource, self).__init__(raw_model, connection)

    @property
    def id(self):
        """str: Gets the Resource ID."""
        return self.raw_model["resourceId"]

    @property
    def description(self):
        """str: Gets the Resource Description."""
        return self.raw_model["description"]

    @description.setter
    def description(self, description):
        self.raw_model["description"] = description

    @property
    def media_type(self):
        """str: Gets the Media type."""
        return self.raw_model["mediaType"]

    @property
    def dataset_id(self):
        """str: Gets the Dataset ID."""
        return self.raw_model["datasetId"]

    @property
    def folder_id(self):
        """str: Gets the Folder ID."""
        return self.raw_model["folderId"]

    @folder_id.setter
    def folder_id(self, folder_id):
        self.raw_model["folderId"] = folder_id

    @property
    def frame_id(self):
        """str: Gets the Frame ID."""
        return self.labels["frame_id"]

    @property
    def storage_id(self):
        """str: Gets the Storage ID."""
        return self.raw_model["storageId"]

    @property
    def name(self):
        """str: Gets the Resource Name."""
        return self.raw_model["name"]

    @name.setter
    def name(self, name):
        self.raw_model["name"] = name

    @property
    def provenance(self):
        """dict: Gets the Provenance."""
        return self.raw_model["provenance"]

    @provenance.setter
    def provenance(self, provenance):
        self.raw_model["provenance"] = provenance

    @property
    def supplier_implied_dt(self):
        """str: Gets the supplier date."""
        return self.labels["supplier_implied_dt"]

    @property
    def type(self):
        """str: Gets the Resource Type."""
        return self.raw_model["type"]

    @property
    def tags(self):
        """:obj:`list` of :obj:`str`: Gets the Resource Tags."""
        return self.raw_model["tags"]

    @tags.setter
    def tags(self, tags):
        self.raw_model["tags"] = tags

    @property
    def labels(self):
        """dict: Gets the Resource labels."""
        labels_dict = {}
        for label in self.raw_model["labels"]:
            labels_dict[label["labelKey"]] = label["labelValue"]
        return labels_dict

    @property
    def as_of(self):
        """str: Gets the as_of."""
        return self.raw_model["asOf"]

    @property
    def created_at(self):
        """str: Gets created_at."""
        return self.raw_model["createdAt"]

    @property
    def ingestion_time(self):
        """str: Gets created_at."""
        return self.labels["ingestion_dt"]

    @property
    def modified_at(self):
        """str: Gets modified_at."""
        return self.raw_model["modifiedAt"]

    @property
    def size(self):
        """int: Gets the size."""
        return self.raw_model["size"]

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

    def delete(self):
        # type: () -> bool
        """Deletes Resource from Dataset.

        Returns:
            bool: True if it is deleted.
        """
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        return self.connection.api_call("DELETE", ["resources", self.id], headers=headers)

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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        body = {}  # type: Dict[str, Union[str, List, Dict]]

        if name is not None:
            self.raw_model["name"] = name
        if description is not None:
            self.raw_model["description"] = description
        if tags is not None:
            self.raw_model["tags"] = tags
        if provenance is not None:
            self.raw_model["provenance"] = provenance

        body = self.raw_model

        log.debug("Body %s", body)

        resource_object = self.connection.api_call(
            "PUT", ["resources", self.id], headers=headers, json=body, model=Resource
        )

        self.raw_model = resource_object.raw_model

        log.debug("Updated dataset %s with content %s", self.id, self.raw_model)
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
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
            "GET", ["resources", self.id, "permissions"], model=Permission, headers=headers,
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})

        labels_list = []
        for label_key, label_value in labels_dict.items():
            if label_key is not None and label_value is not None:
                label_key = label_key.value if isinstance(label_key, Enum) else label_key
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
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
        headers = Headers({"content-type": "application/json", "accept": "application/json"})
        resource_object = self.connection.api_call(
            "GET", ["resources", self.id], headers=headers, model=Resource
        )

        self.raw_model = resource_object.raw_model

        return True


# https://github.com/python/mypy/issues/2477, mypy is performing checking with Python2
class MediaType(Enum):  # type: ignore
    """MediaType Enumeration Model."""

    JSON = "application/json"
    NDJSON = "application/x-ndjson"
    CSV = "text/csv"
    PARQUET = "parquet/binary"
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
