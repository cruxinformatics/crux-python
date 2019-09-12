import copy
import os

import pytest

from crux import Crux
from crux.models import Dataset, File, Identity


def monkeypatch_whoami():

    raw_model = {
        "identityId": "1234",
        "parentIdentityId": "4567",
        "description": "Creating Identity",
        "companyName": "ACME Corp",
        "firstName": "John",
        "lastName": "Doe",
        "role": "Admin",
        "phone": "0000000000",
        "email": "johndoe@acme.com",
        "type": "user",
        "website": "acme.com",
        "landingPage": "acme.com",
    }

    return Identity(raw_model=raw_model)


def monkeypatch_create_dataset(name=None, description=None, tags=None):
    raw_model = {
        "datasetId": "123545",
        "ownerIdentityId": "12342366",
        "contactIdentityId": "123235ewr",
        "name": name,
        "description": description,
        "website": "acme.com",
        "tags": ["tags1"],
    }
    return Dataset(raw_model=raw_model)


def monkeypatch_get_dataset(dataset_id):
    raw_model = {
        "datasetId": "1234",
        "ownerIdentityId": "12342366",
        "contactIdentityId": "123235ewr",
        "name": "my_dataset",
        "description": "dataset_description",
        "website": "acme.com",
        "tags": ["tags1"],
    }
    return Dataset(raw_model=raw_model)


def monkeypatch_call_drives_my():
    return {
        "owned": [
            {
                "datasetId": "0000000001",
                "ownerIdentityId": "12342366",
                "contactIdentityId": "123235ewr",
                "name": "my_dataset",
                "description": "dataset_description",
                "website": "acme.com",
                "createdAt": "",
                "modifiedAt": "",
                "tags": ["tags1"],
            }
        ],
        "subscriptions": [
            {
                "datasetId": "0000000002",
                "ownerIdentityId": "123420987",
                "contactIdentityId": "98735ewz",
                "name": "another_dataset",
                "description": "dataset_description_2",
                "website": "example.com",
                "createdAt": "",
                "modifiedAt": "",
                "tags": ["tags1"],
            },
            {
                "datasetId": "0000000003",
                "ownerIdentityId": "321420987",
                "contactIdentityId": "98655ewz",
                "name": "another__subscribed_dataset",
                "description": "dataset_description_3",
                "website": "widgets.com",
                "createdAt": "",
                "modifiedAt": "",
                "tags": ["tags1"],
            },
        ],
    }


def monkeypatch_get_resource_dict(method, path, model=None, headers=None):
    """Return a fake requests.Response object with a mock .json() method."""

    class MockResponse:
        def json(self):
            resource = {
                "resourceId": path[1],
                "datasetId": "UNIT_TEST_DATASET_ID",
                "description": "UNIT_TEST_DESC",
                "folderId": "UNIT_TEST_FOLDER_ID",
                "folder": "UNIT_TEST_FOLDER",
                "mediaType": "avro/binary",
                "name": "test.avro",
                "size": 512,
                "type": "file",
                "config": {},
                "provenance": {},
                "asOf": "2019-04-23",
                "storageId": "UNIT_TEST_STORAGE_ID",
                "createdAt": "2019-04-23",
                "modifiedAt": "2019-04-23",
                "labels": [
                    {
                        "labelKey": "UNIT_TEST_LABEL_KEY",
                        "labelValue": "UNIT_TEST_LABEL_VALUE",
                    }
                ],
            }
            return resource

    response = MockResponse()
    return response


@pytest.fixture
def monkey_conn():
    os.environ["CRUX_API_KEY"] = "12345"
    return Crux()


def test_whoami(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "whoami", monkeypatch_whoami)
    monkey_identity = monkey_conn.whoami()
    assert monkey_identity.identity_id == "1234"


def test_create_dataset(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "create_dataset", monkeypatch_create_dataset)
    monkey_ds = monkey_conn.create_dataset(
        name="my_dataset", description="Creating Dataset", tags=["tag1", "tag2"]
    )
    assert monkey_ds.name == "my_dataset"


def test_delete_dataset(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "get_dataset", monkeypatch_get_dataset)
    monkey_ds = monkey_conn.get_dataset("1234")
    assert monkey_ds.id == "1234"


def test_list_datasets(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "_call_drives_my", monkeypatch_call_drives_my)
    monkey_datasets = monkey_conn.list_datasets()
    assert len(monkey_datasets) == 3


def test_list_subscribed_datasets(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "_call_drives_my", monkeypatch_call_drives_my)
    monkey_datasets = monkey_conn.list_datasets(owned=False)
    assert len(monkey_datasets) == 2


def test_list_owned_datasets(monkeypatch, monkey_conn):
    monkeypatch.setattr(monkey_conn, "_call_drives_my", monkeypatch_call_drives_my)
    monkey_datasets = monkey_conn.list_datasets(subscribed=False)
    assert len(monkey_datasets) == 1


def test_get_resource(monkeypatch, monkey_conn):
    monkeypatch.setattr(
        monkey_conn.api_client, "api_call", monkeypatch_get_resource_dict
    )
    resource = monkey_conn.get_resource("UNIT_TEST_RESOURCE_ID")
    assert isinstance(resource, File)
    assert resource.id == "UNIT_TEST_RESOURCE_ID"


def test_deepcopy(monkey_conn):
    monkey_copy = copy.deepcopy(monkey_conn)
    assert type(monkey_conn) == type(monkey_copy)
