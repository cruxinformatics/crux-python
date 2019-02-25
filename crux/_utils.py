"""Modules contains set of utility functions."""

import posixpath
from typing import List, Tuple  # noqa: F401 pylint: disable=unused-import

from requests import Session

from crux._compat import urllib_quote


DEFAULT_CHUNK_SIZE = 10485760  # 10 MB


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


def str_to_bool(string):
    # type (str) -> bool
    """Converts string to boolean value.

    Args:
        string (str): Input string.

    Returns:
        bool: True if input string is "True" or "true",
            False if input string is "False" or "false".

    Raises:
        ValueError: If input string is not in True, true,
            False, false.
    """
    if string in ("True", "true"):
        return True
    elif string in ("False", "false"):
        return False
    else:
        raise ValueError("Cannot convert {} to bool".format(string))


class Headers(dict):
    """Headers Dictionary to convert Dictionary keys to lower case."""

    def __init__(self, input_dict):
        # type(dict) -> None
        super(Headers, self).__init__()
        self.update(input_dict)

    def __setitem__(self, key, value):
        # type(str, str) -> None
        lower_key = key.lower()
        super(Headers, self).__setitem__(lower_key, value)

    def __getitem__(self, key):
        # type(str) -> Any
        return self.get(key)

    def update(self, input_dict):
        # type(dict) -> None
        for key, value in input_dict.items():
            self[key.lower()] = value

    def get(self, key):
        # type(str) -> Any
        return super(Headers, self).get(key.lower())


# google.resumable_media.requests.ResumableUpload is only compatible with JSON API endpoint.
# Signed URL uses XML API Endpoint, which requires setting specific headers.
# ResumableUploadSingedSession is added to make google.resumable_media.requests.ResumableUpload
# compatible with XML API endpoint by including XML API endpoint specific headers.
class ResumableUploadSignedSession(Session):
    """Session class to support Resumable Upload."""

    def request(  # pylint: disable=arguments-differ
        self, method, url, data=None, headers=None, **kwargs
    ):
        """Implementation of Requests' request."""

        request_headers = Headers(headers.copy() if headers is not None else {})

        if self.headers:
            request_headers.update(self.headers)

        response = super(ResumableUploadSignedSession, self).request(
            method, url, data=data, headers=request_headers, **kwargs
        )

        return response
