import os
from tempfile import NamedTemporaryFile

import pytest


@pytest.mark.usefixtures("dataset", "helpers")
def test_load_file_into_table(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )

    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    file = dataset.upload_file(path="/" + file_name, local_path=upload_path)

    assert file.name == file_name

    table_config = {
        "schema": [
            {"name": "bank", "type": "string"},
            {"name": "location", "type": "string"},
        ]
    }

    table_name = "bank_table_" + helpers.generate_random_string(4)

    table = dataset.create_table(path="/" + table_name, config=table_config)

    assert table.name == table_name

    job = dataset.load_table_from_file(source_file=file, dest_table=table, append=False)

    assert hasattr(job, "job_id")
    assert hasattr(job, "job_url")


@pytest.mark.usefixtures("dataset", "helpers")
def test_create_run_query(dataset, helpers):
    upload_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "data",
        "test_file.csv",
    )
    file_name = "test_file_" + helpers.generate_random_string(4) + ".csv"

    dataset.upload_file(path="/" + file_name, local_path=upload_path)

    table_config = {
        "schema": [
            {"name": "bank", "type": "string"},
            {"name": "location", "type": "string"},
        ]
    }

    table_name = "bank_table_" + helpers.generate_random_string(4)

    dataset.create_table(path="/" + table_name, config=table_config)

    query_config = {"query": "SELECT * FROM " + table_name}

    query_name = "bank_query" + helpers.generate_random_string(4)

    query = dataset.create_query(path="/" + query_name, config=query_config)

    stream = query.run(format="csv", decode_unicode=True)

    result = ""

    for chunk in stream:
        result += chunk

    assert "bank" in result
    assert "location" in result

    query.delete()


@pytest.mark.usefixtures("dataset", "helpers")
def test_upload_download_query(dataset, helpers):

    table_config = {
        "schema": [
            {"name": "bank", "type": "string"},
            {"name": "location", "type": "string"},
        ]
    }

    dataset.create_table(path="/bank_table_3", config=table_config)

    sql_path = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "data", "query.sql"
    )
    query_name = "bank_query" + helpers.generate_random_string(4)

    query = dataset.upload_query(path="/" + query_name, sql_file=sql_path)

    assert query.name == query_name

    with NamedTemporaryFile() as temp_query_file:
        download_result = query.download(local_path=temp_query_file.name)
        assert download_result is True
