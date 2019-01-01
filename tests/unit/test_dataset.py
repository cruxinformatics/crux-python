import os

import pytest

from crux.client import CruxClient
from crux.models import Dataset, File, Folder, Label, Query, Resource, StitchJob, Table


@pytest.fixture(scope="module")
def dataset():
    os.environ["CRUX_API_KEY"] = "1235"
    conn = CruxClient(crux_config=None)
    dataset = Dataset(
        name="test_dataset", description="test_dataset_description", tags=["tags1"]
    )
    dataset.connection = conn
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
    file_resource = File(
        name="test_file.txt", type="file", tags=tags, description=description
    )
    file_resource.folder = "/folder1/folder2"
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


def monkeypatch_create_table(tags=None, description=None, path=None, config=None):
    table_resource = Table(
        name="test_table",
        type="table",
        tags=tags,
        description=description,
        config=config,
    )
    table_resource.folder = "/folder1/folder2"
    return table_resource


def test_create_table(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "create_table", monkeypatch_create_table)
    config = {"schema": [{"name": "col_name", "type": "string"}]}
    resp = dataset.create_table(
        path="/folder1/folder2/test_table",
        description="test_table_description",
        tags=["tags"],
        config=config,
    )

    assert resp.name == "test_table"
    assert resp.description == "test_table_description"
    assert resp.tags == ["tags"]


def monkeypatch_create_folder(tags=None, description=None, path=None, folder=None):
    folder_resource = Folder(
        name="folder3",
        type="folder",
        tags=["tags"],
        description="test_folder_description",
    )
    folder_resource.folder = "/folder1/folder2"
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
    assert resp.folder == "/folder1/folder2"
    assert resp.description == "test_folder_description"
    assert resp.tags == ["tags"]


def monkeypatch_create_query(
    tags=None, description=None, path=None, folder=None, config=None
):

    query_resource = Query(
        name="bank_query",
        type="query",
        tags=["tags"],
        description="test_query_description",
    )

    query_resource.folder = "/test_folder1/test_folder2"

    return query_resource


def test_create_query(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "create_query", monkeypatch_create_query)
    query_config = {"query": "select * from bank_table"}
    resp = dataset.create_query(
        path="/test_folder1/test_folder2/bank_query",
        tags=["test_tag1", "test_tag2"],
        description="bank_query",
        config=query_config,
    )

    assert resp.name == "bank_query"
    assert resp.folder == "/test_folder1/test_folder2"
    assert resp.description == "test_query_description"
    assert resp.tags == ["tags"]


def monkeypatch_upload_query(
    tags=None, description=None, path=None, folder=None, sql_file=None
):

    query_resource = Query(
        name="bank_query",
        type="query",
        tags=["tags"],
        description="test_query_description",
    )

    query_resource.folder = "/test_folder1/test_folder2"

    return query_resource


def test_upload_query(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "upload_query", monkeypatch_upload_query)
    resp = dataset.upload_query(
        path="/test_folder1/test_folder2/bank_query",
        tags=["test_tag1", "test_tag2"],
        description="bank_query",
        sql_file="/tmp/bank_query.sql",
    )

    assert resp.name == "bank_query"
    assert resp.folder == "/test_folder1/test_folder2"
    assert resp.description == "test_query_description"
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
    return Label(label_key="test_label1", label_value="test_value1")


def test_get_label(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "get_label", monkeypatch_get_label)
    label = dataset.get_label(label_key="test_label1")
    assert label.label_value == "test_value1"
    assert label.label_key == "test_label1"


def monkeypatch_search_label(predicates=None):
    return [
        Resource(
            id="12345",
            dataset_id="4567",
            name="resource1",
            type="file",
            tags=["tag1", "tag2"],
            description="test_resource1",
        ),
        Resource(
            id="12346",
            dataset_id="4567",
            name="resource2",
            type="query",
            tags=["tag1", "tag2"],
            description="test_resource1",
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
        name="test_file.txt", type="file", tags=tags, description=description
    )
    file_resource.folder = "/folder1/folder2"
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
    return StitchJob(job_id=job_id, status="done")


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
    content_type, folder, local_path, description=None, tags=None
):
    return [
        File(
            name="test_file.txt",
            type="file",
            tags=["tags"],
            description="test_description",
        ),
        File(
            name="test_file_2.txt",
            type="file",
            tags=["tags"],
            description="test_description",
        ),
    ]


def test_upload_files(dataset, monkeypatch):
    monkeypatch.setattr(dataset, "upload_files", monkeypatch_upload_files)
    file_list = dataset.upload_files(
        content_type="avro/binary",
        folder="/",
        local_path="/tmp",
        description="test_description",
        tags=["tag1", "tag2"],
    )
    assert len(file_list) == 2
    assert file_list[0].name == "test_file.txt"
    assert file_list[1].name == "test_file_2.txt"


def monkeypatch_update_dataset(*args, **kwargs):
    return Dataset(name="test_dataset1", tags=["tag1"], description="test_description")


def test_update_dataset(dataset, monkeypatch):
    monkeypatch.setattr(dataset.connection, "api_call", monkeypatch_update_dataset)
    update_result = dataset.update(
        name="test_dataset1", description="test_description", tags=["tag1"]
    )
    assert update_result is True

    with pytest.raises(TypeError):
        dataset.update(tags="tag1")

    with pytest.raises(ValueError):
        dataset.update()
