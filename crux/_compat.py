"""Module handles import compatibility issues between Python 2 and Python 3."""
# pylint: disable=useless-suppression,ungrouped-imports

try:
    # Python 3 imports
    from builtins import str as unicode
    from enum import Enum
    from urllib.parse import quote as urllib_quote  # type: ignore
except ImportError:
    # Python 2 imports
    from __builtin__ import unicode  # type: ignore
    from crux._vendor.enum import Enum  # type: ignore
    from urllib import quote as urllib_quote

__all__ = ("Enum", "unicode", "urllib_quote")
