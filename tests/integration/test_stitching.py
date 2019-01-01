import os

import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_stitch_with_file_object(dataset, helpers):
    stitch_file = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "twitter.avro",
    )

    file_1 = dataset.upload_file(
        tags=["test_tag1"],
        description="test_description",
        path="/twitter_" + helpers.generate_random_string(4) + ".avro",
        local_path=stitch_file,
    )

    file_2 = dataset.upload_file(
        tags=["test_tag1"],
        description="test_description",
        path="/twitter_" + helpers.generate_random_string(4) + ".avro",
        local_path=stitch_file,
    )

    file_obj, job_id = dataset.stitch(
        source_resources=[file_1, file_2],
        destination_resource="/test_destination_file.avro",
        labels={"test_label1": "test_value1"},
    )

    assert file_obj.name == "test_destination_file.avro"


@pytest.mark.usefixtures("dataset", "helpers")
def test_stitch(dataset, helpers):
    stitch_file = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "twitter.avro",
    )

    file_1_name = "/twitter_str_" + helpers.generate_random_string(4) + ".avro"

    dataset.upload_file(
        tags=["test_tag1"],
        description="test_description",
        path=file_1_name,
        local_path=stitch_file,
    )

    file_2_name = "/twitter_str_" + helpers.generate_random_string(4) + ".avro"

    dataset.upload_file(
        tags=["test_tag1"],
        description="test_description",
        path=file_2_name,
        local_path=stitch_file,
    )

    file_obj, job_id = dataset.stitch(
        source_resources=[file_1_name, file_2_name],
        destination_resource="/test_destination_str_file.avro",
        labels={"test_label1": "test_value1"},
    )

    assert file_obj.name == "test_destination_str_file.avro"
