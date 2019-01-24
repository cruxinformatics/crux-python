import os

import pytest
import requests
from requests.exceptions import (
    ConnectTimeout,
    HTTPError,
    ProxyError,
    ReadTimeout,
    SSLError,
    TooManyRedirects,
)
from requests.models import Response


from crux.client import CruxClient
from crux.exceptions import (
    CruxClientConnectionError,
    CruxClientHTTPError,
    CruxClientTimeout,
)
from crux.models.model import CruxModel


class SampleModel(CruxModel):
    def __init__(self, attr_1=None, attr_2=None):
        self._attr_1 = None
        self._attr_2 = None

        self.attr_1 = attr_1
        self.attr_2 = attr_2

    @property
    def attr_1(self):
        return self._attr_1

    @attr_1.setter
    def attr_1(self, attr_1):
        self._attr_1 = attr_1

    @property
    def attr_2(self):
        return self._attr_2

    @attr_2.setter
    def attr_2(self, attr_2):
        self._attr_2 = attr_2

    @classmethod
    def from_dict(cls, a_dict):
        """Method which transforms SampleModel Dictionary to SampleModel object

            Args:
                cls(SampleModel): SampleModel Class
                a_dict(dict): SampleModel Dictionary
            Returns:
                SampleModel(SampleModel): SampleModel Object
        """
        attr_1 = a_dict["attr1"]
        attr_2 = a_dict["attr2"]

        return cls(attr_1=attr_1, attr_2=attr_2)

    def to_dict(self):
        """ Method which transforms SampleModel object to SampleModel Dictionary

        Args:
            self: SampleModel instance Object
        Returns:
            Resource(dict): SampleModel Dictionary
        """
        return {"attr_1": self.attr_1, "attr_2": self.attr_2}


@pytest.fixture
def client():
    os.environ["CRUX_API_KEY"] = "1235"
    return CruxClient(crux_config=None)


def monkeypatch_delete_call(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    json=None,
    data=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    delete_resp = Response()
    delete_resp.status_code = 204
    return delete_resp


def test_client_delete(client, monkeypatch):
    monkeypatch.setattr(requests.sessions.Session, "request", monkeypatch_delete_call)
    resp = client.api_call(
        method="DELETE", path=["test-path"], model=None, headers=None
    )

    assert resp is True


def monkeypatch_get_call_with_no_model(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    json=None,
    data=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = b'{"data":"dummy"}'
    return get_resp


def test_client_get_with_no_model(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session, "request", monkeypatch_get_call_with_no_model
    )
    resp = client.api_call(method="GET", path=["test-path"], model=None, headers=None)

    assert resp.json() == {"data": "dummy"}


def monkeypatch_get_call(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    json=None,
    data=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = b'{"attr1":"dummy1","attr2":"dummy2"}'
    return get_resp


def test_client_get_with_model(client, monkeypatch):
    monkeypatch.setattr(requests.sessions.Session, "request", monkeypatch_get_call)

    resp = client.api_call(method="GET", path=["test-path"], model=SampleModel)

    assert resp.attr_1 == "dummy1"
    assert resp.attr_2 == "dummy2"


def monkeypatch_post_call(
    self,
    method=None,
    url=None,
    headers=None,
    stream=False,
    params=None,
    data=None,
    json=None,
    proxies=None,
    timeout=None,
):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = b'{"attr1":"dummy1","attr2":"dummy2"}'
    return get_resp


def test_client_post(client, monkeypatch):
    monkeypatch.setattr(requests.sessions.Session, "request", monkeypatch_post_call)
    sample_obj = SampleModel(attr_1="attr1", attr_2="attr2")
    resp = client.api_call(
        method="POST", path=["test-path"], model=SampleModel, json=sample_obj.to_dict()
    )

    assert resp.attr_1 == "dummy1"
    assert resp.attr_2 == "dummy2"


def monkeypatch_put_call(
    self,
    method=None,
    url=None,
    headers=None,
    stream=False,
    json=None,
    params=None,
    data=None,
    proxies=None,
    timeout=None,
):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = b'{"attr1":"dummy1","attr2":"dummy2"}'
    return get_resp


def test_client_put(client, monkeypatch):
    monkeypatch.setattr(requests.sessions.Session, "request", monkeypatch_put_call)
    sample_obj = SampleModel(attr_1="attr1", attr_2="attr2")
    resp = client.api_call(
        method="PUT", path=["test-path"], model=SampleModel, json=sample_obj.to_dict()
    )

    assert resp.attr_1 == "dummy1"
    assert resp.attr_2 == "dummy2"


def monkeypatch_get_list_call(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = (
        b'[{"attr1":"dummy1","attr2":"dummy2"},{"attr1":"dummy3","attr2":"dummy4"}]'
    )
    return get_resp


def test_client_get_list_with_model(client, monkeypatch):
    monkeypatch.setattr(requests.sessions.Session, "request", monkeypatch_get_list_call)

    resp = client.api_call(method="GET", path=["test-path"], model=SampleModel)

    assert resp[0].attr_1 == "dummy1"
    assert resp[0].attr_2 == "dummy2"
    assert resp[1].attr_1 == "dummy3"
    assert resp[1].attr_2 == "dummy4"


def monkeypatch_client_http_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise HTTPError("Test HTTP Error")


def test_client_http_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session, "request", monkeypatch_client_http_exception
    )

    with pytest.raises(CruxClientHTTPError):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)


def monkeypatch_test_client_proxy_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise ProxyError("Test Proxy Error")


def test_client_proxy_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session, "request", monkeypatch_test_client_proxy_exception
    )

    with pytest.raises(CruxClientConnectionError):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)


def monkeypatch_test_client_ssl_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise SSLError("Test Proxy Error")


def test_client_ssl_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session, "request", monkeypatch_test_client_ssl_exception
    )

    with pytest.raises(CruxClientConnectionError):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)


def monkeypatch_test_client_connect_timeout_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise ConnectTimeout("Test Connect Timeout Error")


def test_client_connect_timeout_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session,
        "request",
        monkeypatch_test_client_connect_timeout_exception,
    )

    with pytest.raises(CruxClientTimeout):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)


def monkeypatch_test_client_read_timeout_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise ReadTimeout("Test Connect Timeout Error")


def test_client_read_timeout_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session,
        "request",
        monkeypatch_test_client_read_timeout_exception,
    )

    with pytest.raises(CruxClientTimeout):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)


def monkeypatch_test_too_many_redirects_exception(
    self,
    method=None,
    url=None,
    headers=None,
    params=None,
    data=None,
    json=None,
    stream=False,
    proxies=None,
    timeout=None,
):
    raise TooManyRedirects("Test Connect Timeout Error")


def test_client_too_many_redirects_exception(client, monkeypatch):
    monkeypatch.setattr(
        requests.sessions.Session,
        "request",
        monkeypatch_test_too_many_redirects_exception,
    )

    with pytest.raises(CruxClientHTTPError):
        client.api_call(method="GET", path=["test-path"], model=SampleModel)
