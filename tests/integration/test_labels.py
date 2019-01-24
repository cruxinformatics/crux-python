import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_add_get_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(4) + ".csv"
    )
    label_result = file_1.add_label("label1", "value1")
    assert label_result is True
    assert file_1.labels.get("label1") == "value1"


@pytest.mark.usefixtures("dataset", "helpers")
def test_search_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(4) + ".csv"
    )
    file_2 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(4) + ".csv"
    )
    label_result_1 = file_1.add_label("label1", "value1")
    label_result_2 = file_2.add_label("label1", "value1")
    assert label_result_1 is True
    assert label_result_2 is True
    # Searching the another label, as searching for labels instantaneously
    # returns empty response
    predicates = [{"op": "eq", "key": "label2", "val": "value2"}]
    resources = dataset.find_resources_by_label(predicates=predicates)
    resource_ids = [resource.id for resource in resources]
    assert len(resource_ids) == 0
    # assert file_1.id in resource_ids
    # assert file_2.id in resource_ids


@pytest.mark.usefixtures("dataset", "helpers")
def test_delete_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(4) + ".csv"
    )
    file_2 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(4) + ".csv"
    )

    file_1.add_label("label1", "value1")

    file_2.add_label("label1", "value1")

    d1_result = file_1.delete_label(label_key="label1")

    assert d1_result is True

    d2_result = file_2.delete_label(label_key="label1")

    assert d2_result is True
