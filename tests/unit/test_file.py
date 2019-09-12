import pytest

from crux.models import File, Permission


@pytest.fixture(scope="module")
def file():
    return File(
        raw_model={
            "name": "test_file",
            "type": "file",
            "tags": ["tags"],
            "description": "test_description",
        }
    )


def test_file_name(file):
    assert file.name == "test_file"


def test_file_description(file):
    assert file.description == "test_description"


def test_file_tags(file):
    assert file.tags == ["tags"]


def test_file_type(file):
    assert file.type == "file"


def monkeypatch_add_permission():
    return Permission(
        raw_model={
            "identityId": "_subscribed_",
            "permissionName": "Read",
            "targetId": "12345",
        }
    )


def monkeypatch_list_permissions():
    return [
        Permission(
            raw_model={
                "identityId": "_subscribed_",
                "permissionName": "Read",
                "targetId": "12345",
            }
        )
    ]


def test_add_permission(monkeypatch, file):
    monkeypatch.setattr(file, "add_permission", monkeypatch_add_permission)
    perm_obj = file.add_permission()
    assert perm_obj.permission_name == "Read"
    assert perm_obj.target_id == "12345"


def test_list_permission(monkeypatch, file):
    monkeypatch.setattr(file, "list_permissions", monkeypatch_list_permissions)
    perm_list = file.list_permissions()
    assert perm_list[0].permission_name == "Read"
    assert perm_list[0].target_id == "12345"


def monkeypatch_read():
    yield "crux"
    yield "informatics"


def test_iter_content(monkeypatch, file):
    monkeypatch.setattr(file, "iter_content", monkeypatch_read)
    data = []
    stream = file.iter_content()
    for content in stream:
        data.append(content)
    assert data == ["crux", "informatics"]


def monkeypatch_download(local_path):
    return True


def test_download(monkeypatch, file):
    monkeypatch.setattr(file, "download", monkeypatch_download)
    result = file.download("/tmp/test.csv")
    assert result is True
