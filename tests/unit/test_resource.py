import os

import pytest
from requests.models import Response

from crux._client import CruxClient
from crux.models import Permission, Resource


@pytest.fixture(scope="module")
def resource():
    os.environ["CRUX_API_KEY"] = "1235"
    conn = CruxClient(crux_config=None)
    resource = Resource(
        name="test_file", type="file", tags=["tags"], description="test_description"
    )
    resource.connection = conn
    return resource


def test_resource_name(resource):
    assert resource.name == "test_file"


def test_resource_description(resource):
    assert resource.description == "test_description"


def test_resource_tags(resource):
    assert resource.tags == ["tags"]


def test_resource_type(resource):
    assert resource.type == "file"


def monkeypatch_add_permission():
    return Permission(
        identity_id="_subscribed_", permission_name="Read", target_id="12345"
    )


def monkeypatch_list_permissions():
    return [
        Permission(
            identity_id="_subscribed_", permission_name="Read", target_id="12345"
        )
    ]


def test_add_permission(monkeypatch, resource):
    monkeypatch.setattr(resource, "add_permission", monkeypatch_add_permission)
    perm_obj = resource.add_permission()
    assert perm_obj.permission_name == "Read"
    assert perm_obj.target_id == "12345"


def test_list_permission(monkeypatch, resource):
    monkeypatch.setattr(resource, "list_permissions", monkeypatch_list_permissions)
    perm_list = resource.list_permissions()
    assert perm_list[0].permission_name == "Read"
    assert perm_list[0].target_id == "12345"


def monkeypatch_delete_resource():
    return {}


def test_delete_resource(monkeypatch, resource):
    monkeypatch.setattr(resource, "delete", monkeypatch_delete_resource)
    resp = resource.delete()
    assert resp == {}


def monkeypatch_add_label(label_key=None, label_value=None):
    return {}


def test_add_label(resource, monkeypatch):
    monkeypatch.setattr(resource, "add_label", monkeypatch_add_label)
    resp = resource.add_label(label_key="test_label1", label_value="test_value1")
    assert resp == {}


def monkeypatch_add_labels_true(*args, **kwargs):
    return True  # api_call returns an object or bool


def test_add_labels_true(resource, monkeypatch):
    monkeypatch.setattr(resource.connection, "api_call", monkeypatch_add_labels_true)
    resp = resource.add_labels(labels_dict={"test_label1": "test_value1"})
    assert resp is True


def monkeypatch_add_labels_false(*args, **kwargs):
    return False  # api_call returns an object or bool


def test_add_labels_false(resource, monkeypatch):
    monkeypatch.setattr(resource.connection, "api_call", monkeypatch_add_labels_false)
    resp = resource.add_labels(labels_dict={"test_label1": "test_value1"})
    assert resp is False


def monkeypatch_delete_label(label_key=None):
    return {}


def test_delete_label(resource, monkeypatch):
    monkeypatch.setattr(resource, "delete_label", monkeypatch_delete_label)
    resp = resource.delete_label(label_key="test_label1")

    assert resp == {}


def monkeypatch_update_resource(*args, **kwargs):
    get_resp = Response()
    get_resp.status_code = 200
    get_resp._content = (
        b'{"name": "test_dataset2","description": "test_description","tags": ["tag1"]}'
    )
    return get_resp


def test_update_resource(resource, monkeypatch):
    monkeypatch.setattr(resource.connection, "api_call", monkeypatch_update_resource)
    update_result = resource.update(
        name="test_dataset1", description="test_description", tags=["tag1"], 
        provenance='{"raw_resource_id": ["resource_id1", "resource_id2"]}'
    )
    assert update_result is True

    with pytest.raises(TypeError):
        resource.update(tags="tag1")

    with pytest.raises(ValueError):
        resource.update()
