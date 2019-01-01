import pytest

from crux.models import Permission


@pytest.fixture(scope="module")
def permission():
    return Permission(
        identity_id="_subscribed_", permission_name="Read", target_id="12345"
    )


def test_permission_identity_id(permission):
    assert permission.identity_id == "_subscribed_"


def test_permission_name(permission):
    assert permission.permission_name == "Read"


def test_permission_target_id(permission):
    assert permission.target_id == "12345"
