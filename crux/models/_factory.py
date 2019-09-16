"""Module contains functions to create Resource objects."""

from typing import Any, Dict, Union  # noqa: F401

from crux._client import CruxClient
from crux.models.file import File
from crux.models.folder import Folder


def get_resource_object(resource_type, data, connection=None):
    # type: (str, Dict[str, Any], CruxClient) -> Union[File, Folder]
    """Creates resource object based on its type.

    Args:
        resource_type (str): Type of resource which needs to be created.
        data (dict): Dictionary which contains serialized resource data.
        connection (CruxClient): Connection Object. Defaults to None.

    Returns:
        crux.models.Resource: Resource or its Child Object.

    Raises:
        TypeError: If it is unable to detect resource type.
    """
    if resource_type == "file":
        return File.from_dict(data, connection=connection)
    elif resource_type == "folder":
        return Folder.from_dict(data, connection=connection)
    else:
        raise TypeError("Invalid Resource Type")
