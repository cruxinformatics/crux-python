import pytest

from crux.models import Folder


@pytest.fixture(scope="module")
def folder():
    return Folder(
        raw_model={
            "name": "my_folder",
            "type": "folder",
            "tags": ["tags"],
            "description": "my_folder_description",
        }
    )


def test_folder_name(folder):
    assert folder.name == "my_folder"


def test_folder_tags(folder):
    assert folder.tags == ["tags"]


def test_folder_description(folder):
    assert folder.description == "my_folder_description"
