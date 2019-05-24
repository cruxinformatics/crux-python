"""
Module packages root level crux objects.
"""
import logging
from logging import NullHandler

from crux._utils import TRACE
from crux.apis import Crux

__all__ = ("Crux", "TRACE")

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
