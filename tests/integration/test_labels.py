import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_add_get_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    label_result = file_1.add_label("label1", "value1")
    assert label_result is True
    assert file_1.labels.get("label1") == "value1"


@pytest.mark.usefixtures("dataset", "helpers")
def test_add_labels_set_labels(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    labels = {"label1": "value1", "label2": "value2"}
    labels_result = file_1.add_labels(labels)
    assert labels_result is True
    assert file_1.labels == labels


# Negative Test case which verifies label search by searching unset labels without pagination.
@pytest.mark.usefixtures("dataset", "helpers")
def test_search_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    file_2 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    label_result_1 = file_1.add_label("label1", "value1")
    label_result_2 = file_2.add_label("label1", "value1")
    assert label_result_1 is True
    assert label_result_2 is True
    predicates = [{"op": "eq", "key": "label4", "val": "value4"}]
    resources = dataset.find_resources_by_label(predicates=predicates)
    resource_ids = [resource.id for resource in resources]
    assert len(resource_ids) == 0


# Negative Test case which verifies label search by searching unset labels with pagination.
@pytest.mark.usefixtures("dataset", "helpers")
def test_search_label_page(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    file_2 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    label_result_1 = file_1.add_label("label2", "value2")
    label_result_2 = file_2.add_label("label2", "value2")
    assert label_result_1 is True
    assert label_result_2 is True
    predicates = [{"op": "eq", "key": "label3", "val": "value3"}]
    resources = dataset.find_resources_by_label(predicates=predicates, max_per_page=1)
    resource_ids = [resource.id for resource in resources]
    assert len(resource_ids) == 0


@pytest.mark.usefixtures("dataset", "helpers")
def test_delete_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )
    file_2 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    file_1.add_label("label1", "value1")

    file_2.add_label("label1", "value1")

    d1_result = file_1.delete_label(label_key="label1")

    assert d1_result is True

    d2_result = file_2.delete_label(label_key="label1")

    assert d2_result is True


def test_update_field_label(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    file_1.add_label("label1", "value1")

    file_1.description = "new_description"

    file_1.update()

    file_1.refresh()

    assert file_1.description == "new_description"

    assert file_1.labels.get("label1") == "value1"


def test_labels_update(dataset, helpers):
    file_1 = dataset.create_file(
        path="/test_file_" + helpers.generate_random_string(16) + ".csv"
    )

    file_1.add_label("label1", "value1")

    assert file_1.labels["label1"] == "value1"

    file_1.labels["label2"] = "value2"

    file_1.update()

    assert len(file_1.labels) == 2
    assert file_1.labels["label2"] == "value2"

    file_1.labels = {"label3": "value3"}

    file_1.update()

    assert len(file_1.labels) == 3
    assert file_1.labels["label3"] == "value3"

    file_1.refresh()

    assert len(file_1.labels) == 3
