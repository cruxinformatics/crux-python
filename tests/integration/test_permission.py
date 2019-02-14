import os

import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_file_add_delete_permission(dataset, helpers):
    file_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_1 = dataset.upload_file(
        file_path, "/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    permission = file_1.add_permission()

    assert permission.identity_id == "_subscribed_"
    assert permission.permission_name == "Read"

    delete_permission_result = file_1.delete_permission()

    file_perms = file_1.list_permissions()

    assert delete_permission_result is True

    for perm in file_perms:
        assert perm.permission_name in ["Admin"]

    file_1.delete()


@pytest.mark.skip(reason="Test is too slow")
@pytest.mark.usefixtures("dataset", "helpers")
def test_folder_add_delete_permission(dataset, helpers):
    file_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_1 = dataset.upload_file(
        file_path,
        "/test_folder/test_file_" + helpers.generate_random_string(16) + ".csv",
    )
    file_2 = dataset.upload_file(
        file_path,
        "/test_folder/test_file_" + helpers.generate_random_string(16) + ".csv",
    )

    folder_1 = dataset.get_folder(path="/test_folder")

    permission_result = folder_1.add_permission(recursive=True)

    assert permission_result is True

    file_1_perms = file_1.list_permissions()
    file_2_perms = file_1.list_permissions()

    assert len(file_1_perms) == 2
    assert len(file_2_perms) == 2

    for perm in file_1_perms:
        assert perm.permission_name in ["Read", "Admin"]

    for perm in file_2_perms:
        assert perm.permission_name in ["Read", "Admin"]

    delete_permission_result = folder_1.delete_permission(recursive=True)

    assert delete_permission_result is True

    file_1_perms = file_1.list_permissions()
    file_2_perms = file_1.list_permissions()

    for perm in file_1_perms:
        assert perm.permission_name in ["Admin"]

    for perm in file_1_perms:
        assert perm.permission_name in ["Admin"]

    file_1.delete()
    file_2.delete()
    folder_1.delete()


@pytest.mark.usefixtures("dataset", "helpers")
def test_dataset_add_permission(dataset, helpers):
    file_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_1 = dataset.upload_file(
        file_path, "/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    file_2 = dataset.upload_file(
        file_path,
        "/test_folder/test_file_" + helpers.generate_random_string(16) + ".csv",
    )

    file_3 = dataset.upload_file(
        file_path,
        "/test_folder/test_file_" + helpers.generate_random_string(16) + ".csv",
    )

    dataset_perm_result = dataset.add_permission()

    assert dataset_perm_result is True

    for file_object in [file_1, file_2, file_3]:
        perm_list = file_object.list_permissions()
        assert len(perm_list) == 2
        for perm_object in perm_list:
            assert perm_object.permission_name in ["Admin", "Read"]

    dataset_perm_result = dataset.delete_permission()

    assert dataset_perm_result is True

    for file_object in [file_1, file_2, file_3]:
        perm_list = file_object.list_permissions()
        assert len(perm_list) == 1
        for perm_object in perm_list:
            assert perm_object.permission_name in ["Admin"]
