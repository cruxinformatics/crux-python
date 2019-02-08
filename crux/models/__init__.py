"""
Module containing models that represent objects returned by the API.
"""

import logging
from logging import NullHandler

from crux.models.dataset import Dataset
from crux.models.file import File
from crux.models.folder import Folder
from crux.models.identity import Identity
from crux.models.job import Job, LoadJob, StitchJob
from crux.models.label import Label
from crux.models.permission import Permission
from crux.models.query import Query
from crux.models.resource import Resource
from crux.models.table import Table


__all__ = (
    "Identity",
    "Permission",
    "LoadJob",
    "StitchJob",
    "Job",
    "Resource",
    "File",
    "Folder",
    "Table",
    "Dataset",
    "Query",
    "Label",
)

# Set default logging handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(NullHandler())
