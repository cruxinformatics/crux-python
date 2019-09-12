"""
Module containing models that represent objects returned by the API.
"""

import logging
from logging import NullHandler

from crux.models.dataset import Dataset
from crux.models.delivery import Delivery
from crux.models.file import File
from crux.models.folder import Folder
from crux.models.identity import Identity
from crux.models.ingestion import Ingestion
from crux.models.job import Job, StitchJob
from crux.models.label import Label
from crux.models.permission import Permission
from crux.models.resource import Resource


__all__ = (
    "Identity",
    "Permission",
    "StitchJob",
    "Job",
    "Resource",
    "File",
    "Folder",
    "Dataset",
    "Label",
    "Delivery",
    "Ingestion",
)

# Set default logging handler to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(NullHandler())
