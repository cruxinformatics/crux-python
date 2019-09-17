import os

import pytest

from crux import Crux


@pytest.mark.usefixtures("connection")
def test_whoami(connection):
    identity = connection.whoami()
    assert identity.type == "user"


def test_whoami_inline(monkeypatch):
    api_host = os.getenv("CRUX_API_HOST")
    api_key = os.getenv("CRUX_API_KEY")
    monkeypatch.delenv("CRUX_API_HOST", raising=False)
    monkeypatch.delenv("CRUX_API_KEY", raising=False)
    connection = Crux(api_host=api_host, api_key=api_key)
    identity = connection.whoami()
    assert identity.type == "user"


def test_api_key_required(monkeypatch):
    monkeypatch.delenv("CRUX_API_HOST", raising=False)
    monkeypatch.delenv("CRUX_API_KEY", raising=False)
    with pytest.raises(ValueError):
        Crux()
