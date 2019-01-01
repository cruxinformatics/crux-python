"""Module contains Resource model."""

from typing import (  # noqa: F401 pylint: disable=unused-import
    Any,
    Dict,
    List,
    Tuple,
    Union,
)

from requests.models import Response  # noqa: F401 pylint: disable=unused-import

from crux.compat import unicode
from crux.models.label import Label
from crux.models.model import CruxModel
from crux.models.permission import Permission
from crux.utils import DEFAULT_CHUNK_SIZE, valid_chunk_size


class Resource(CruxModel):
    """Resource Model."""

    def __init__(
        self,
        id=None,  # type: str # id name is by design pylint: disable=redefined-builtin
        dataset_id=None,  # type: str
        folder_id=None,  # type: str
        name=None,  # type: str
        size=None,  # type: str
        type=None,  # type: str # type name is by design pylint: disable=redefined-builtin
        config=None,  # type: Dict[str, Any]
        provenance=None,  # type: str
        as_of=None,  # type: str
        created_at=None,  # type: str
        modified_at=None,  # type: str
        storage_id=None,  # type: str
        description=None,  # type: str
        media_type=None,  # type: str
        tags=None,  # type: List[str]
        labels=(),  # type: Tuple[Label,...]
        connection=None,
        raw_response=None,  # type: Dict[Any, Any]
    ):
        # type: (...) -> None
        """
        Attributes:
            id (str): Resourece Id. Defaults to None.
            dataset_id (str): Dataset Identity. Defaults to None.
            folder_id (str): Folder Identity. Defaults to None.
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
            labels (:obj:`list` of :obj:`crux.models.Label`): List of Label objects.
                Defaults to None.
            connection (crux.client.CruxClient): Connection Object. Defaults to None.
            raw_response (dict): Response Content. Defaults to None.

        Raises:
            ValueError: If name or tags are set to None.
            TypeError: If tags are not of list type.
        """
        self._id = None
        self._dataset_id = None
        self._folder_id = None
        self._description = None
        self._name = None
        self._size = None
        self._type = None
        self._config = None
        self._provenance = None
        self._as_of = None
        self._created_at = None
        self._storage_id = None
        self._media_type = None
        self._modified_at = None
        self._tags = None
        self._folder = None
        self._labels = labels  # type: Tuple[Label, ...]

        self.id = id
        self.dataset_id = dataset_id
        self.folder_id = folder_id
        self.name = name
        self.size = size
        self.type = type
        self.config = config
        self.provenance = provenance
        self.as_of = as_of
        self.created_at = created_at
        self.modified_at = modified_at
        self.storage_id = storage_id
        self.connection = connection
        self.raw_response = raw_response
        self.media_type = media_type
        self.description = description
        self.tags = tags

    @property
    def id(self):
        """str: Gets and Sets the Resource ID."""
        return self._id

    @id.setter
    def id(self, id):  # id name is by design pylint: disable=redefined-builtin
        self._id = id

    @property
    def description(self):
        """str: Gets and Sets the Resource Description."""
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def media_type(self):
        """str: Gets and Sets the Resource Description."""
        return self._media_type

    @media_type.setter
    def media_type(self, media_type):
        self._media_type = media_type

    @property
    def dataset_id(self):
        """str: Gets and Sets the Dataset ID."""
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, dataset_id):
        self._dataset_id = dataset_id

    @property
    def folder_id(self):
        """str: Gets and Sets the Folder ID."""
        return self._folder_id

    @folder_id.setter
    def folder_id(self, folder_id):
        self._folder_id = folder_id

    @property
    def storage_id(self):
        """str: Gets and Sets the Storage ID."""
        return self._storage_id

    @storage_id.setter
    def storage_id(self, storage_id):
        self._storage_id = storage_id

    @property
    def name(self):
        """str: Gets and Sets the Resource Name."""
        return self._name

    @name.setter
    def name(self, name):
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        self._name = name

    @property
    def config(self):
        """str: Gets and Sets the config."""
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def provenance(self):
        """str: Gets and Sets the Provenance."""
        return self._provenance

    @provenance.setter
    def provenance(self, provenance):
        self._provenance = provenance

    @property
    def type(self):
        """str: Gets and Sets the Resource Type."""
        return self._type

    @type.setter
    def type(self, type):  # type name is by design pylint: disable=redefined-builtin
        self._type = type

    @property
    def tags(self):
        """:obj:`list` of :obj:`str`: Gets and Sets the Resource Tags."""
        return self._tags

    @tags.setter
    def tags(self, tags):
        if not isinstance(tags, list):
            raise TypeError("Invalid Type for `tags`, tags should be of type list")
        self._tags = tags

    @property
    def labels(self):
        """:obj:`list` of :obj:`dict`: Gets and Sets the Resource labels."""
        return tuple(self._labels)

    @property
    def as_of(self):
        """str: Gets and Sets the as_of."""
        return self._as_of

    @as_of.setter
    def as_of(self, as_of):
        self._as_of = as_of

    @property
    def created_at(self):
        """str: Gets and Sets the created_at."""
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @property
    def modified_at(self):
        """str: Gets and Sets the modified_at."""
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        self._modified_at = modified_at

    def to_dict(self):
        # type: () -> Dict[str, Any]
        """Transforms Resource object to Resource Dictionary.

        Returns:
            dict: Resource Dictionary.
        """
        return {
            "resourceId": self.id,
            "datasetId": self.dataset_id,
            "description": self.description,
            "folderId": self.folder_id,
            "mediaType": self.media_type,
            "name": self.name,
            "size": self.size,
            "type": self.type,
            # "config": self.config,
            # "provenance": self.provenance,
            "asof": self.as_of,
            "tags": self.tags,
            "labels": self.labels,
            "storageId": self.storage_id,
            "createdAt": self.created_at,
            "modifiedAt": self.modified_at,
        }

    @classmethod
    def from_dict(cls, a_dict):
        # type: (Dict[str, Any]) -> Any
        """Transforms Resource Dictionary to Resource object.

        Args:
            a_dict (dict): Resource Dictionary.

        Returns:
            crux.models.Resource: Resource Object.
        """
        id = a_dict[  # id name is by design pylint: disable=redefined-builtin
            "resourceId"
        ]
        dataset_id = a_dict["datasetId"]
        description = a_dict["description"]
        folder_id = a_dict["folderId"]
        storage_id = a_dict["storageId"]
        media_type = a_dict["mediaType"]
        description = a_dict["description"]
        name = a_dict["name"]
        # Added to provide compatibility with normal objects and Stitching objects,
        # till the time it is resolved
        if "tags" in a_dict:
            tags = a_dict["tags"]
        else:
            tags = []
        type = a_dict[  # type name is by design pylint: disable=redefined-builtin
            "type"
        ]
        # Added to provide compatibility with normal objects and Stitching objects,
        # till the time it is resolved
        if "config" in a_dict:
            config = a_dict["config"]
        else:
            config = None
        if "labels" in a_dict:
            labels = []
            for label in a_dict["labels"]:
                labels.append(Label.from_dict(label))
        else:
            labels = []
        provenance = a_dict["provenance"]
        created_at = a_dict["createdAt"]
        modified_at = a_dict["modifiedAt"]

        return cls(
            dataset_id=dataset_id,
            id=id,
            folder_id=folder_id,
            media_type=media_type,
            storage_id=storage_id,
            description=description,
            name=name,
            tags=tags,
            labels=tuple(labels),
            type=type,
            config=config,
            provenance=provenance,
            created_at=created_at,
            modified_at=modified_at,
        )

    def delete(self):
        # type: () -> bool
        """Deletes Resource from Dataset.

        Returns:
            bool: True if it is deleted.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return self.connection.api_call(
            "DELETE", ["resources", self.id], headers=headers
        )

    def update(self, name=None, description=None, tags=None):
        # type: (str, str, List[str]) -> bool
        """Updates the metadata for Resource.

        Args:
            name (str): Name of resource. Defaults to None.
            description (str): Description of the resource. Defaults to None.
            tags (:obj:`list` of :obj:`str`): List of tags. Default to None.

        Returns:
            bool: True, if resource is updated.

        Raises:
            ValueError: It is raised if name, description or tags are unset.
            TypeError: It is raised if tags are not of type List.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        params = {}  # type: Dict[str, Union[str, List, Dict]]

        if name is not None:
            params["name"] = name
        if description is not None:
            params["description"] = description
        if tags is not None:
            if isinstance(tags, list):
                params["tags"] = tags
            else:
                raise TypeError("Tags should be of type list")

        if params:
            response = self.connection.api_call(
                "PUT", ["resources", self.id], headers=headers, params=params
            )

            response_dict = response.json()

            if "name" in response_dict:
                self.name = response.json().get("name")
            if "response" in response_dict:
                self.tags = response.json().get("tags")
            if "description" in response_dict:
                self.description = response.json().get("description")
            return True
        else:
            raise ValueError("Name, Description or Tags should be set")

    def _download(self, local_path, content_type, chunk_size=DEFAULT_CHUNK_SIZE):
        if content_type is not None:
            headers = {"Accept": content_type}
        else:
            headers = None

        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        data = self.connection.api_call(
            "GET", ["resources", self.id, "content"], headers=headers, stream=True
        )

        if hasattr(local_path, "write"):
            for chunk in data.iter_content(chunk_size=chunk_size):
                local_path.write(chunk)
            local_path.flush()
            return True
        elif isinstance(local_path, (str, unicode)):
            with open(local_path, mode="wb") as local_file:
                for chunk in data.iter_content(chunk_size=chunk_size):
                    local_file.write(chunk)
            return True
        else:
            raise TypeError(
                "Invalid Data Type for local_path: {}".format(type(local_path))
            )

    def download(self, local_path, content_type=None, chunk_size=DEFAULT_CHUNK_SIZE):
        # type: (...) -> bool
        """Downloads the resource.

        Args:
            local_path (str or file): Local OS path at which resource will be downloaded.
            content_type (str): Content Type of resource to be downloaded.
                Defaults to None.
            chunk_size (int): Number of bytes to be read in memory.

        Returns:
            bool: True if it is downloaded.

        Raises:
            ValueError: If chunk size is not multiple of 256 KB.
            TypeError: If local_path is not str or file object.
        """
        if not valid_chunk_size(chunk_size):
            raise ValueError("chunk_size should be multiple of 256 KiB")

        return self._download(
            local_path=local_path, content_type=content_type, chunk_size=chunk_size
        )

    def add_permission(self, identity_id="_subscribed_", permission="Read"):
        # type: (str, str) -> Union[bool, Permission]
        """Adds permission to the resource.

        Args:
            identity_id: Identity Id to be set. Defaults to _subscribed_.
            permission: Permission to be set. Defaults to Read.

        Returns:
            crux.models.Permission: Permission Object.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return self.connection.api_call(
            "PUT",
            ["permissions", self.id, identity_id, permission],
            model=Permission,
            headers=headers,
        )

    def delete_permission(self, identity_id="_subscribed_", permission="Read"):
        # type: (str, str) -> bool
        """Deletes permission from the resource.

        Args:
            identity_id (str): Identity Id for the deletion.
                Defaults to _subscribed_.
            permission (str): Permission for the deletion.
                Defaults to Read.

        Returns:
            bool: True if it is able to delete it.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return self.connection.api_call(
            "DELETE", ["permissions", self.id, identity_id, permission], headers=headers
        )

    def list_permissions(self):
        # type: () -> List[Permission]
        """Lists the permission on the resource.

        Returns:
            list (:obj:`crux.models.Permission`): List of Permission Objects.
        """
        headers = {"Accept": "application/json"}
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
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
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
            self._labels = self._labels + (Label(label_key, label_value),)
            return True
        else:
            return False

    def delete_label(self, label_key):
        # type: (str) -> bool
        """Deletes label from Resource.

        Args:
            label_key (str): Label Key for Resource.

        Returns:
            bool: True if label is deleted, False otherwise.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response_result = self.connection.api_call(
            "DELETE",
            ["datasets", self.dataset_id, "resources", self.id, "labels", label_key],
            headers=headers,
        )

        if response_result:
            for index, label in enumerate(self.labels):
                if label.label_key == label_key:
                    labels_list = list(self._labels)  # type: List[Label]
                    labels_list.pop(index)
                    self._labels = tuple(labels_list)
            return True
        else:
            return False

    def get_label(self, label_key):
        # type: (str) -> Label
        """Gets label value of Resource.

        Args:
            label_key (str): Label Key for Resource.

        Returns:
            crux.models.Label: Label Object.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        return self.connection.api_call(
            "GET",
            ["datasets", self.dataset_id, "resources", self.id, "labels", label_key],
            headers=headers,
            model=Label,
        )

    def get_all_labels(self):
        # type: () -> Tuple[Label, ...]
        """Fetches all labels of the Resource.

        Returns:
            list (:obj:`crux.models.Label`): List of Label Objects.
        """
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = self.connection.api_call(
            "GET", ["resources", self.id, "labels"], headers=headers
        )

        label_objects = []  # type: List[Label]

        labels = response.json().get("labels")

        if labels:
            for label in labels:
                obj = Label.from_dict(label)
                label_objects.append(obj)

        label_tuple_obj = tuple(label_objects)  # type: Tuple[Label, ...]
        return label_tuple_obj
