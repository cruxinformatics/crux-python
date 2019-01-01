"""Module provides CruxConfig object to manage API configuration settings."""

import os
import platform
import re
from typing import (  # noqa: F401 pylint: disable=unused-import
    Dict,
    MutableMapping,
    Optional,
    Text,
    Union,
)

import requests

from crux.__version__ import __version__


class CruxConfig(object):
    """
    Crux Configuration Class.
    """

    def __init__(
        self,
        api_key=None,  # type: Optional[str]
        api_host=None,  # type: str
        api_prefix=None,  # type: str
        proxies=None,  # type: Optional[MutableMapping[Text, Text]]
        user_agent=None,  # type: str
    ):
        # type: (...) -> None
        """
        Args:
            api_key (str): API Key. Defaults to None.
            api_host (str): API URL. Defaults to None.
            api_prefix (str): API prefix to be used. Defaults to None.
            proxies (dict): Proxies to be used. Defaults to None.
            user_agent (str): User agent to be used. Defaults to None.

        Raises:
            ValueError: If CRUX_AP_KEY is not set.
        """
        self.re_user_agent_banned_chars = re.compile(r"[^a-zA-Z0-9._+~-]")
        self.re_whitespace_runs = re.compile(r"\s+")

        if api_key is None:
            if "CRUX_API_KEY" in os.environ:
                self.api_key = os.environ.get("CRUX_API_KEY")  # type: Optional[str]
            else:
                raise ValueError("API KEY is required")
        else:
            self.api_key = api_key  # type: Optional[str]

        if api_host is None:
            self.api_host = os.environ.get(
                "CRUX_API_HOST", "https://api.cruxinformatics.com"
            )
        else:
            self.api_host = api_host

        if api_prefix is None:
            self.api_prefix = os.environ.get("CRUX_API_PREFIX", "plat-api")
        else:
            self.api_prefix = api_prefix

        if user_agent is None:
            self.user_agent = self._default_user_agent()
        else:
            self.user_agent = user_agent

        self.proxies = (
            proxies if proxies else {}
        )  # type: Optional[MutableMapping[Text, Text]]

    def _default_user_agent(self):
        # type: () -> str
        user_agent = (
            "crux-python/{ver}"
            " requests/{req_ver} {py_impl}/{py_ver} "
            "{os}/{os_ver} {cpu}/{machine}"
        ).format(
            ver=__version__,
            req_ver=self._sanitize_user_agent_part(requests.__version__),
            py_impl=self._sanitize_user_agent_part(platform.python_implementation()),
            py_ver=self._sanitize_user_agent_part(platform.python_version()),
            os=self._sanitize_user_agent_part(platform.system()),
            os_ver=self._sanitize_user_agent_part(platform.release()),
            cpu=self._sanitize_user_agent_part(platform.processor()),
            machine=self._sanitize_user_agent_part(platform.machine()),
        )

        return user_agent

    def _sanitize_user_agent_part(self, part):
        # type: (str) -> str
        if part:
            no_space_part = self.re_whitespace_runs.sub("_", part)
            sanitized_part = self.re_user_agent_banned_chars.sub("", no_space_part)
            if sanitized_part:
                return sanitized_part
        return "unknown"
