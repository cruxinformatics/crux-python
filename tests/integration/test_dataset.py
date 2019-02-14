import pytest

from crux.exceptions import CruxAPIError


@pytest.mark.usefixtures("connection", "helpers")
def test_create_get_delete_dataset(connection, helpers):
    dataset_name = "crux_py_dataset_" + helpers.generate_random_string(6)
    dataset = connection.create_dataset(
        name=dataset_name, description="test_description"
    )
    assert dataset.name == dataset_name
    assert dataset.description == "test_description"
    d1 = connection.get_dataset(id=dataset.id)
    assert d1.id == dataset.id
    assert d1.name == dataset_name
    assert d1.description == "test_description"
    dataset.delete()
    with pytest.raises(CruxAPIError):
        dataset.delete()


@pytest.mark.usefixtures("connection")
def test_whoami(connection):
    identity = connection.whoami()
    assert identity.type == "user"


@pytest.mark.skip(reason="Test is flaky")
@pytest.mark.usefixtures("connection", "dataset")
def test_set_datasets_provenance(connection, dataset):
    provenance = {
        dataset.id: [
            {
                "workflowId": "test_id",
                "pipeline_ids": ["test_id_1", "test_id_2"],
                "cronSpec": "0 0 1 1 0",
            }
        ]
    }
    response = connection.set_datasets_provenance(provenance)

    assert bool(response) is True
    assert dataset.provenance[0]["workflowId"] == "test_id"


@pytest.mark.usefixtures("connection", "helpers")
def test_dataset_description_limit(connection, helpers):
    description_too_long = helpers.generate_random_string(2049)
    dataset_name = "crux_py_dataset_" + helpers.generate_random_string(6)
    with pytest.raises(CruxAPIError) as dataset_des_long_exception:
        connection.create_dataset(name=dataset_name, description=description_too_long)
    assert dataset_des_long_exception.value.status_code == 400


@pytest.mark.usefixtures("connection", "helpers")
def test_dataset_name_limit(connection, helpers):
    dataset_name_too_long = helpers.generate_random_string(500)
    with pytest.raises(CruxAPIError) as dataset_name_long_exception:
        connection.create_dataset(
            name=dataset_name_too_long, description="test description"
        )
    assert dataset_name_long_exception.value.status_code == 400


@pytest.mark.usefixtures("connection", "dataset")
def test_recreate_dataset_name(connection, dataset):
    with pytest.raises(CruxAPIError) as dataset_duplicate_name_exception:
        connection.create_dataset(name=dataset.name, description="test_description")
    assert dataset_duplicate_name_exception.value.status_code == 409
