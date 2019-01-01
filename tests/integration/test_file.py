import os

import pytest

from crux.exceptions import CruxResourceNotFoundError


@pytest.mark.usefixtures("dataset", "helpers")
def test_stream_file(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )
    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file_1 = dataset.upload_file(local_path=upload_path, path="/" + file_name)

    assert file_1.name == file_name

    stream = file_1.iter_content(decode_unicode=True)

    result = ""

    for chunk in stream:
        result += chunk

    assert "bank" in result
    assert "location" in result


@pytest.mark.usefixtures("dataset", "helpers")
def test_delete_file(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file_1 = dataset.upload_file(local_path=upload_path, path="/" + file_name)

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
        "/test_file_" + helpers.generate_random_string(4) + ".csv"
    )

    upload_result = file_1.upload(upload_file_string)

    assert upload_result is True


@pytest.mark.usefixtures("dataset", "helpers")
def test_upload_file_object(dataset, helpers):
    upload_file_string = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_os_object = open(upload_file_string, "rb")

    file_1 = dataset.create_file(
        "/test_file_" + helpers.generate_random_string(4) + ".csv"
    )

    upload_result = file_1.upload(file_os_object)

    assert upload_result is True

    file_os_object.close()
