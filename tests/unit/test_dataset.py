import os

import pytest

from crux._client import CruxClient
from crux.models import Dataset, Delivery, File, Folder, Label, Resource, StitchJob


@pytest.fixture(scope="module")
def dataset():
    os.environ["CRUX_API_KEY"] = "1235"
    conn = CruxClient(crux_config=None)
    raw_model = {
        "datasetId": "12345",
        "name": "test_dataset",
        "description": "test_dataset_description",
        "tags": ["tags1"],
    }
    dataset = Dataset(raw_model=raw_model, connection=conn)
    return dataset


def test_dataset_name(dataset):
    assert dataset.name == "test_dataset"


def test_dataset_description(dataset):
    assert dataset.description == "test_dataset_description"


def monkeypatch_delete_dataset():
    return {}


def test_dataset_delete(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "delete", monkeypatch_delete_dataset)
    resp = dataset.delete()
    assert resp == {}


def monkeypatch_create_file(tags=None, description=None, path=None):

    raw_model = {
        "name": "test_file.txt",
        "type": "file",
        "tags": tags,
        "description": description,
    }
    file_resource = File(raw_model=raw_model)
    return file_resource


def test_create_file(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "create_file", monkeypatch_create_file)
    resp = dataset.create_file(
        path="/folder1/folder2/test_file.txt",
        description="test_file_description",
        tags=["tags"],
    )

    assert resp.name == "test_file.txt"
    assert resp.description == "test_file_description"
    assert resp.tags == ["tags"]


def monkeypatch_create_folder(tags=None, description=None, path=None, folder=None):

    raw_model = {
        "name": "folder3",
        "type": "folder",
        "tags": ["tags"],
        "description": "test_folder_description",
    }
    folder_resource = Folder(raw_model=raw_model)
    return folder_resource


def test_create_folder(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "create_folder", monkeypatch_create_folder)
    # monkeypatch.setattr(dataset.connection, "api_call", monkeypatch_create_folder)
    resp = dataset.create_folder(
        folder="/folder1/folder2",
        path="folder3",
        description="test_folder_description",
        tags=["tags"],
    )

    assert resp.name == "folder3"
    assert resp.description == "test_folder_description"
    assert resp.tags == ["tags"]


def monkeypatch_add_label(label_key=None, label_value=None):
    return {}


def test_add_label(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "add_label", monkeypatch_add_label)
    resp = dataset.add_label(label_key="test_label1", label_value="test_value1")

    assert resp == {}


def monkeypatch_delete_label(label_key=None):
    return {}


def test_delete_label(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "delete_label", monkeypatch_delete_label)
    resp = dataset.delete_label(label_key="test_label1")

    assert resp == {}


def monkeypatch_get_label(label_key=None):
    raw_model = {"labelKey": "test_label1", "labelValue": "test_value1"}
    return Label(raw_model=raw_model)


def test_get_label(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "get_label", monkeypatch_get_label)
    label = dataset.get_label(label_key="test_label1")
    assert label.label_value == "test_value1"
    assert label.label_key == "test_label1"


def monkeypatch_search_label(predicates=None):
    return [
        Resource(
            raw_model={
                "resourceId": "12345",
                "datasetId": "4567",
                "name": "resource1",
                "type": "file",
                "tags": ["tag1", "tag2"],
                "description": "test_resource1",
            }
        ),
        Resource(
            raw_model={
                "resourceId": "12346",
                "datasetId": "4567",
                "name": "resource2",
                "type": "file",
                "tags": ["tag1", "tag2"],
                "description": "test_resource1",
            }
        ),
    ]


def test_search_label(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "find_resources_by_label", monkeypatch_search_label)
    resource_list = dataset.find_resources_by_label()
    assert resource_list[0].id == "12345"
    assert resource_list[0].name == "resource1"
    assert resource_list[1].id == "12346"
    assert resource_list[1].name == "resource2"


def monkeypatch_stitch(
    source_resources, destination_resource, labels=None, tags=None, description=None
):
    file_resource = File(
        raw_model={
            "name": "test_file.txt",
            "type": "file",
            "tags": tags,
            "description": description,
        }
    )
    return file_resource, "123456"


def test_stitch(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "stitch", monkeypatch_stitch)
    file_resource, job_id = dataset.stitch(
        source_resources=["/folder1/folder2/test_file.txt"],
        destination_resource="/test_output.txt",
        labels={"label1": "value1"},
        tags=["tags1"],
        description="test_description",
    )
    assert file_resource.name == "test_file.txt"
    assert file_resource.description == "test_description"
    assert job_id == "123456"


def monkeypatch_get_stitch_job(job_id=None):
    return StitchJob(raw_model={"jobId": job_id, "status": "done"})


def test_get_stitch_job(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "get_stitch_job", monkeypatch_get_stitch_job)
    job = dataset.get_stitch_job(job_id="123456")
    assert job.job_id == "123456"
    assert job.status == "done"


def monkeypatch_download_files(folder, local_path):
    return ["/tmp/file_1.csv", "/tmp/file_2.csv"]


def test_download_files(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "download_files", monkeypatch_download_files)
    file_path_list = dataset.download_files(folder="/", local_path="/tmp")
    assert len(file_path_list) == 2
    assert file_path_list[0] == "/tmp/file_1.csv"
    assert file_path_list[1] == "/tmp/file_2.csv"


def monkeypatch_upload_files(
    media_type, folder, local_path, description=None, tags=None
):
    return [
        File(
            raw_model={
                "name": "test_file.txt",
                "type": "file",
                "tags": ["tags"],
                "description": "test_description",
            }
        ),
        File(
            raw_model={
                "name": "test_file_2.txt",
                "type": "file",
                "tags": ["tags"],
                "description": "test_description",
            }
        ),
    ]


def test_upload_files(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "upload_files", monkeypatch_upload_files)
    file_list = dataset.upload_files(
        media_type="avro/binary",
        folder="/",
        local_path="/tmp",
        description="test_description",
        tags=["tag1", "tag2"],
    )
    assert len(file_list) == 2
    assert file_list[0].name == "test_file.txt"
    assert file_list[1].name == "test_file_2.txt"


def monkeypatch_get_delivery(*args, **kwargs):
    return Delivery(
        raw_model={
            "latest_health_status": "DELIVERY_SUCCEEDED",
            "delivery_id": "abcd123.1",
            "dataset_id": "12345",
        }
    )


def test_get_delivery(dataset, monkeypatch):
    monkeypatch.setattr(dataset.connection, "api_call", monkeypatch_get_delivery)
    delivery_object = dataset.get_delivery("abcd123.1")
    assert delivery_object.id == "abcd123.1"

def monkeypatch_get_ingestions(*args, **kwargs):
    class MockResponse:
        def json(self):
            delivery_list = ["abcd123.0", "abcd123.1", "xyz123.0"]
            return delivery_list

    response = MockResponse()
    return response


def test_get_ingestions(dataset, monkeypatch):
    monkeypatch.setattr(dataset.connection, "api_call", monkeypatch_get_ingestions)
    ingestions = dataset.get_ingestions()
    for ingestion in ingestions:
        if ingestion.id == "abcd123":
            assert ingestion.versions == [0, 1]
        if ingestion.id == "xyz123":
            assert ingestion.versions == [0]
