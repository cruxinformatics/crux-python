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

    folder_name = "{random}".format(random=helpers.generate_random_string(8))
    folder_path = "/{folder}".format(folder=folder_name)

    file_objects = dataset.upload_files(local_path=data_dir, folder=folder_path)
    assert len(file_objects) == 2
    for file_object in file_objects:
        assert file_object.name in ["test_file.csv", "test_file_2.csv"]
    download_dir = mkdtemp()
    downloaded_file_list_gen = dataset.download_files(
        local_path=download_dir, folder=folder_path
    )

    downloaded_file_list = [downloaded_file for downloaded_file in downloaded_file_list_gen]
    assert len(downloaded_file_list) == 2
    download_path = os.path.join(download_dir, "test_file.csv")
    assert sorted(downloaded_file_list)[0] == download_path
    download_path2 = os.path.join(download_dir, "test_folder1", "test_file_2.csv")
    assert sorted(downloaded_file_list)[1] == download_path2

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
    file_path = "/{folder}/{file}".format(
        folder=helpers.generate_random_string(8), file=file_name
    )

    with open(upload_path, "rb") as local_file_object:
        file_1 = dataset.upload_file(local_file_object, file_path)

    assert file_1.name == file_name


@pytest.mark.usefixtures("dataset", "helpers")
def test_download_file_object(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file_1 = dataset.upload_file(upload_path, "/test_folder_3/" + file_name)

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

    file_1 = dataset.upload_file(upload_path, "/test_folder_3/" + file_name)

    with NamedTemporaryFile() as temp_file:
        download_result = file_1.download(temp_file.name)
        assert download_result is True

    file_1.delete()
