"""Module contains functions to create Resource objects."""

from typing import Any, Dict, Union  # noqa: F401

from crux.models.file import File
from crux.models.folder import Folder
from crux.models.query import Query
from crux.models.table import Table


def get_resource_object(resource_type, data):
    # type: (str, Dict[str, Any]) -> Union[File, Folder, Query, Table]
    """Creates resource object based on its type.

    Args:
        resource_type (str): Type of resource which needs to be created.
        data (dict): Dictionary which contains serialized resource data.

    Returns:
        crux.models.Resource: Resource or its Child Object.

    Raises:
        TypeError: If it is unable to detect resource type.
    """
    if resource_type == "file":
        return File.from_dict(data)
    elif resource_type == "folder":
        return Folder.from_dict(data)
    elif resource_type == "query":
        return Query.from_dict(data)
    elif resource_type == "table":
        return Table.from_dict(data)
    else:
        raise TypeError("Invalid Resource Type")
