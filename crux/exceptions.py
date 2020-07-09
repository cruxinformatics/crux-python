"""Module contains the set of crux-python's exceptions."""

from typing import Dict, Union  # noqa: F401

import requests  # pylint: disable=unused-import


class CruxAPIError(Exception):
    """Exception which should be raised when the API response expects an error."""

    def __init__(self, message):
        # type: (Dict[str, Union[str, int]]) -> None
        """
        Args:
            message (str): Human readable string describing the exception.

        Attributes:
            message (str): Human readable string describing the exception.
            status_code (int): Exception error code.
        """
        super(CruxAPIError, self).__init__(message)
        # domainV2 has "status"
        self.status_code = message.get("statusCode", message.get("status"))
        self.message = message

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxClientError(Exception):
    """Exception which should be raised when the client SDK expects an error."""

    def __init__(self, message):
        # type: (str) -> None
        """
        Args:
            message (str): Human readable string describing the exception.

        Attributes:
            message (str): Human readable string describing the exception.
        """
        super(CruxClientError, self).__init__(message)
        self.message = message

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxClientHTTPError(CruxClientError):
    """Exception should be raised when SDK expects any HTTP related errors."""

    def __init__(self, message, response):
        # type: (str, requests.Response) -> None
        """
        Args:
            message (str): Human readable string describing the exception.
            response (requests.Response): Response object.

        Attributes:
            message (str): Human readable string describing the exception.
            response (requests.Response): Response object.
        """
        super(CruxClientHTTPError, self).__init__(message)
        self.message = message
        self.response = response

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxClientTooManyRedirects(CruxClientError):
    """Exception should be raised when SDK gets too many redirects."""

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxClientConnectionError(CruxClientError):
    """Exception should be raised when SDK expects any connection related errors."""

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxClientTimeout(CruxClientError):
    """Exception should be raised when SDK expects any timeout related errors."""

    def __str__(self):
        return "{message}".format(message=self.message)


class CruxResourceNotFoundError(CruxAPIError):
    """Exception which should be raised when Crux Resource is not found."""

    def __init__(self, message):
        # type: (Dict[str, Union[str, int]]) -> None
        """
        Args:
            message (str): Human readable string describing the exception.

        Attributes:
            message (str): Human readable string describing the exception.
            status_code (int): Exception error code.
        """
        super(CruxResourceNotFoundError, self).__init__(message)
        self.message = message

    def __str__(self):
        return "{message}".format(message=self.message)
