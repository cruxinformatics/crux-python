import os
import shutil
from tempfile import mkdtemp, NamedTemporaryFile, TemporaryFile

import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_upload_download_files(dataset, helpers):
    data_dir = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "upload_test",
    )

    file_objects = dataset.upload_files(local_path=data_dir, folder="/upload_download")
    assert len(file_objects) == 2
    for file_object in file_objects:
        assert file_object.name in ["test_file.csv", "test_file_2.csv"]
    download_dir = mkdtemp()
    downloaded_file_list = dataset.download_files(
        local_path=download_dir, folder="/upload_download"
    )
    assert len(downloaded_file_list) == 2
    assert sorted(downloaded_file_list)[0] == download_dir + "/test_file.csv"
    assert (
        sorted(downloaded_file_list)[1]
        == download_dir  # noqa: W503 as it is formatted by black
        + "/test_folder1/test_file_2.csv"  # noqa: W503 as it is formatted by black
    )

    assert sorted(os.listdir(data_dir)) == sorted(os.listdir(download_dir))
    shutil.rmtree(download_dir)


@pytest.mark.usefixtures("dataset", "helpers")
def test_upload_file_object(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    local_file_object = open(upload_path, "rb")

    file_1 = dataset.upload_file(
        local_path=local_file_object, path="/test_folder_3/" + file_name
    )

    assert file_1.name == file_name

    local_file_object.close()


@pytest.mark.usefixtures("dataset", "helpers")
def test_download_file_object(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file_1 = dataset.upload_file(
        local_path=upload_path, path="/test_folder_3/" + file_name
    )

    with TemporaryFile() as temp_file:
        download_result = file_1.download(temp_file)
        assert download_result is True

    file_1.delete()


@pytest.mark.usefixtures("dataset", "helpers")
def test_download_file_string(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file_1 = dataset.upload_file(
        local_path=upload_path, path="/test_folder_3/" + file_name
    )

    with NamedTemporaryFile() as temp_file:
        download_result = file_1.download(temp_file.name)
        assert download_result is True

    file_1.delete()
