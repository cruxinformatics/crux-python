import pytest

from crux.models import Table


@pytest.fixture(scope="module")
def table():
    config = {"schema": [{"name": "col_name", "type": "string"}]}
    return Table(
        name="my_table",
        type="table",
        tags=["tags"],
        description="my_table_description",
        config=config,
    )


def test_folder_name(table):
    assert table.name == "my_table"


def test_folder_tags(table):
    assert table.tags == ["tags"]


def test_folder_description(table):
    assert table.description == "my_table_description"
