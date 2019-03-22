"""Module contains code pertaining to CruxClient."""

import logging
from typing import (  # noqa: F401 pylint: disable=unused-import
    Any,
    Dict,
    List,
    MutableMapping,
    Optional,
    Text,
    Tuple,
    Union,
)

from requests.exceptions import (
    ConnectTimeout,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)

from crux._config import CruxConfig
from crux._utils import Headers, url_builder
from crux.exceptions import (
    CruxAPIError,
    CruxClientConnectionError,
    CruxClientHTTPError,
    CruxClientTimeout,
    CruxResourceNotFoundError,
)


log = logging.getLogger(__name__)


class CruxClient(object):
    """Crux HTTP REST client."""

    def __init__(self, crux_config):
        # type: (CruxConfig) -> None
        if crux_config is None:
            log.debug("crux_config is None, initializing CruxConfig object")
            self.crux_config = CruxConfig()  # type: CruxConfig
        else:
            log.debug("Using the passed crux_config object")
            self.crux_config = crux_config  # type: CruxConfig

    def api_call(  # pylint: disable=too-many-branches, too-many-statements
        self,
        method,  # type: str
        path,  # type: List[str]
        model=None,  # type: Any
        headers=None,  # type: MutableMapping[Text, Text]
        params=None,  # type: Dict[Any,Any]
        json=None,  # type: Dict[Any,Any]
        data=None,  # type: Dict[Any,Any]
        stream=False,  # type: bool
        connect_timeout=9.5,  # type: float
        read_timeout=60,  # type: float
    ):
        # type:(...) -> Any
        """
        Requests and Serializes response from API Backend.

        Args:
            method (str): REST method name.
            path (str): API resource path.
            model (crux.models.CruxModel): Deserialization Model. Defaults to None.
            headers (dict): Additonal header parameters. Defaults to None.
            json (dict): Body data to be passed with request. Defaults to None.
            params (dict): Data to be passed in query string. Defaults to None.
            data (dict): Should be used while passing form encoded data. Defaults to None.
            stream (bool): Should be set to True, when response is required to be streamed.
                Defaults to False.
            connect_timeout (float): Request connect timeout configuration in seconds.
                Defaults to 60.5.
            read_timeout (float): Request read timeout configuration in seconds.
                Defaults to 60.

        Returns:
            crux.models.Model or bool: Serialized response from API backend.

        Raises:
            TypeError: If Path is not of list type.
            CruxClientHTTPError: If there is HTTP related error.
            CruxClientConnectionError: If there is SSL or Proxy related error.
            CruxClientTimeout: If there is timout related error.
            CruxResourceNotFoundError: If API has status code 400.
            CruxAPIError: If API has status code other than 2XX.
        """

        if path is None or not isinstance(path, list):
            raise TypeError("Path cannot be of NoneType. It should be of Type List")

        url = url_builder(
            url_base=self.crux_config.api_host,
            url_prefix=self.crux_config.api_prefix,
            url_path_list=path,
        )

        if headers is None:
            headers = Headers({})

        if params is None:
            params = {}

        auth_scheme = "Bearer"  # type: str
        bearer_token = "{scheme} {key}".format(
            scheme=auth_scheme, key=self.crux_config.api_key
        )  # type: Text

        user_agent = self.crux_config.user_agent  # type: Text

        headers["authorization"] = bearer_token
        headers["user-agent"] = user_agent

        session = self.crux_config.session

        if method in ("GET", "DELETE", "PUT", "POST"):
            try:
                log.debug("Setting request stream: %s", stream)
                log.debug("Setting request data: %s, json: %s", data, json)
                log.debug("Setting request params: %s", params)
                response = session.request(
                    method,
                    url,
                    headers=headers,
                    data=data,
                    json=json,
                    stream=stream,
                    params=params,
                    timeout=(connect_timeout, read_timeout),
                )
            except (HTTPError, TooManyRedirects) as err:
                raise CruxClientHTTPError(str(err))
            except (ProxyError, SSLError) as err:
                raise CruxClientConnectionError(str(err))
            except (ConnectTimeout, ReadTimeout) as err:
                raise CruxClientTimeout(str(err))
        else:
            raise ValueError("Request Method Type should be in GET, DELETE, PUT, POST")

        if response.status_code in (200, 201, 202, 206):
            if model is None:
                log.debug("Model is set to None, returning response dictionary")
                return response
            else:
                if isinstance(response.json(), list):
                    log.debug("Response is list of type %s", model)
                    serial_list = []
                    for item in response.json():
                        obj = model.from_dict(item)
                        obj.connection = self
                        obj.raw_response = response.json()
                        serial_list.append(obj)
                    return serial_list

                else:
                    log.debug("Response is of type %s", model)
                    obj = model.from_dict(response.json())
                    obj.connection = self
                    obj.raw_response = response.json()
                    return obj
        elif response.status_code == 204:
            log.debug("Response code is 204, returning True boolean value")
            return True
        else:
            if response.status_code == 404:
                raise CruxResourceNotFoundError(response.json())
            raise CruxAPIError(response.json())

    def close(self):
        """Closes the Session."""
        self.crux_config.session.close()
