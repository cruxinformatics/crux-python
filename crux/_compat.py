"""Module handles import compatibility issues between Python 2 and Python 3."""
# pylint: disable=useless-suppression,ungrouped-imports

try:
    # Python 3 imports
    from builtins import str as unicode
    from urllib.parse import quote as urllib_quote  # type: ignore
except ImportError:
    # Python 2 imports
    from __builtin__ import unicode  # type: ignore
    from urllib import quote as urllib_quote

from enum import Enum

__all__ = ("Enum", "unicode", "urllib_quote")
