"""Modules contains set of utility functions."""

import os
import posixpath
from typing import List, Tuple  # noqa: F401 pylint: disable=unused-import

from crux.compat import Enum, urllib_quote


DEFAULT_CHUNK_SIZE = 10485760  # 10 MB


# https://github.com/python/mypy/issues/2477, mypy is performing checking with Python2
class ContentType(Enum):  # type: ignore
    """ContentType Enumeration Model."""

    JSON = "application/json"
    NDJSON = "application/x-ndjson"
    CSV = "text/csv"
    PARQUET = "application/parquet"
    AVRO = "avro/binary"

    @classmethod
    def detect(cls, file_name):
        # type: (str) -> str
        """Detects the content_type from the file extension.

        Args:
            file_name (str): Absolute or Relative Path of the file.

        Returns:
            str: ContentType extension.

        Raises:
            LookupError: If file type is not supported.
        """
        file_ext = os.path.splitext(file_name)[1][1:].upper()

        if file_ext in cls.__members__:
            return cls[file_ext].value  # type: ignore
        else:
            raise LookupError("File/Media Type not supported.")


def quote(data):
    # type: (str) -> str
    """Percent Encodes the string.

    Args:
        data (str): String which is required to be Percent Encoded.

    Returns:
        str: Percent encoded string.
    """

    # With current setting, it will encode all necessary characters.
    # To prevent any character from getting percent encoded, add it to safe_characters
    # For eg: safe_characters="/%$"
    # https://docs.python.org/2/library/urllib.html
    safe_characters = ""
    return urllib_quote(data, safe=safe_characters)


def url_builder(url_base, url_prefix, url_path_list):
    # type: (str, str, List[str]) -> str
    """Builds Valid Percent Encoded URL.

    Args:
        url_base (str): Base of URL comprised of HTTP protocol scheme and Hostname.
        url_prefix (str): URL Prefix used by API Platform.
        url_path_list (:obj:`list` of :obj:`str`): List of Context Path elements.

    Returns:
        str: Valid Percent Encoded URL.
    """
    if url_prefix:
        valid_url = [url_base, quote(url_prefix)]
    else:
        valid_url = [url_base]

    valid_url_path_list = []

    for component in url_path_list:
        valid_url_path_list.append(quote(component))

    valid_url.extend(valid_url_path_list)

    return "/".join(valid_url)


def valid_chunk_size(chunk_size):
    # type: (int) -> bool
    """Checks whether chunk size is multiple of 256 KiB.

    Args:
        chunk_size (int): Input chunk_size to be validated.

    Returns:
        bool: True if chunk_size is multiple of 256 KiB, False otherwise.
    """
    return not bool(chunk_size % 262144)  # 1024*256=262144


def split_posixpath_filename_dirpath(path):
    # type: (str) -> Tuple[str, str]
    """Split a POSIX path into file name and directory path.

    Args:
        path (str): POSIX path to split.

    Returns:
        (str, str): Returns a tuple of (file name, directory path) with
            trailing slash removed from directory.
    """

    filename = posixpath.basename(path)  # type: str
    dirpath = posixpath.dirname(path)  # type: str
    return filename, dirpath
