import os

import pytest

from crux.__version__ import __version__
from crux._config import CruxConfig


@pytest.fixture
def config_env():
    os.environ["CRUX_API_KEY"] = "12345"
    os.environ["CRUX_API_HOST"] = "https://api-env.example.com"
    os.environ["CRUX_API_PREFIX"] = "/example-v1"
    os.environ["CRUX_ONLY_USE_CRUX_DOMAINS"] = "True"
    return CruxConfig()


def test_env_api_key(config_env):
    assert config_env.api_key == "12345"


def test_env_api_host(config_env):
    assert config_env.api_host == "https://api-env.example.com"


def test_env_api_prefix(config_env):
    assert config_env.api_prefix == "/example-v1"


def test_default_proxies(config_env):
    assert config_env.proxies == {}


def test_default_user_agent(config_env):
    user_agent = config_env._default_user_agent().split()[0]
    assert user_agent == "crux-python/{version}".format(version=__version__)


def test_sanitize_user_agent_part(config_env):
    part = r"""{])`'"/\!@#$%^&*()=Clean  0.1-_+~"""
    sanitized_part = config_env._sanitize_user_agent_part(part)
    assert sanitized_part == "Clean_0.1-_+~"


def test_env_use_crux_domain(config_env):
    assert config_env.only_use_crux_domains is True


@pytest.fixture
def config_def():
    return CruxConfig(
        api_host="http://api-def.example.com",
        api_key="34567",
        api_prefix="/example-v2",
        proxies={
            "http": "socks5://user:pass@host:port",
            "https": "socks5://user:pass@host:port",
        },
        user_agent="crux/browser",
        only_use_crux_domains=True,
    )


def test_def_api_key(config_def):
    assert config_def.api_key == "34567"


def test_def_api_host(config_def):
    assert config_def.api_host == "http://api-def.example.com"


def test_def_api_prefix(config_def):
    assert config_def.api_prefix == "/example-v2"


def test_def_user_agent(config_def):
    assert config_def.user_agent == "crux/browser"


def test_def_proxies(config_def):
    assert config_def.proxies == {
        "http": "socks5://user:pass@host:port",
        "https": "socks5://user:pass@host:port",
    }


def test_def_use_crux_domain(config_def):
    assert config_def.only_use_crux_domains is True
