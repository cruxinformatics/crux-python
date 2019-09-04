import os

import pytest

from crux.exceptions import CruxResourceNotFoundError
from crux.models import File


@pytest.mark.usefixtures("dataset_with_crux_domain", "helpers")
def test_upload_file_string_with_crux_domain(dataset_with_crux_domain, helpers):
    upload_file_string = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_1 = dataset_with_crux_domain.create_file(
        "/test_file_" + helpers.generate_random_string(4) + ".csv"
    )

    uploaded_object = file_1.upload(upload_file_string)

    assert uploaded_object.name == file_1.name


@pytest.mark.usefixtures("dataset_with_crux_domain", "helpers")
def test_upload_file_object_with_crux_domain(dataset_with_crux_domain, helpers):
    upload_file_string = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_os_object = open(upload_file_string, "rb")

    file_1 = dataset_with_crux_domain.create_file(
        "/test_file_" + helpers.generate_random_string(4) + ".csv"
    )

    uploaded_object = file_1.upload(file_os_object)

    assert uploaded_object.name == file_1.name


@pytest.mark.usefixtures("dataset", "helpers")
def test_stream_file(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )
    file_name = "test_file_" + helpers.generate_random_string(16) + ".csv"

    file_1 = dataset.upload_file(upload_path, "/" + file_name)

    assert file_1.name == file_name

    stream = file_1.iter_content()

    result = ""

    for chunk in stream:
        result += chunk.decode("utf-8")

    assert "bank" in result
    assert "location" in result


@pytest.mark.usefixtures("dataset", "helpers")
def test_delete_file(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(16) + ".csv"

    file_1 = dataset.upload_file(upload_path, "/" + file_name)

    assert file_1.name == file_name

    delete_result = file_1.delete()

    assert delete_result is True

    with pytest.raises(CruxResourceNotFoundError):
        file_1.delete()


@pytest.mark.usefixtures("dataset", "helpers")
def test_upload_file_string(dataset, helpers):
    upload_file_string = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_1 = dataset.create_file(
        "/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    uploaded_object = file_1.upload(upload_file_string)

    assert uploaded_object.name == file_1.name


@pytest.mark.usefixtures("connection", "dataset", "helpers")
def test_upload_file_object(connection, dataset, helpers):
    upload_file_string = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_os_object = open(upload_file_string, "rb")

    file_1 = dataset.create_file(
        "/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    uploaded_object = file_1.upload(file_os_object)

    # Test that resources can be fetched by ID
    file_from_id = connection.get_resource(file_1.id)

    assert uploaded_object.name == file_1.name
    assert isinstance(file_from_id, File)
    assert file_from_id.id == file_1.id
    assert file_from_id.size == file_1.size


@pytest.mark.usefixtures("dataset", "helpers")
def test_update_file(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(16) + ".csv"

    file_1 = dataset.upload_file(upload_path, "/" + file_name)

    file_1.description = "new_test_description"
    file_1.tags = ["tag1", "tag2"]
    file_1.update()
    assert file_1.description == "new_test_description"
    file_1.description = "new_2_test_description"
    file_1.refresh()
    assert file_1.description == "new_test_description"
