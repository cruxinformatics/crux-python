import pytest

from crux.utils import (
    ContentType,
    quote,
    split_posixpath_filename_dirpath,
    url_builder,
    valid_chunk_size,
)


def test_quote():
    quoted = r"%21%23%24%26%27%28%29%2A%2B%2C%2F%3A%3B%3D%3F%40%5B%5D%25%20"
    assert quoted == quote(r"""!#$&'()*+,/:;=?@[]% """)


def test_url_builder():
    url = r"https://api.cruxinformatics.com/%5Bplatapi/re%24ource/12%2F%25%2652%2A/c%40ntent"
    built_url = url_builder(
        url_base=r"https://api.cruxinformatics.com",
        url_prefix=r"[platapi",
        url_path_list=[r"re$ource", r"12/%&52*", r"c@ntent"],
    )

    assert url == built_url


def test_valid_chunk_size():
    assert valid_chunk_size(10485760) is True
    assert valid_chunk_size(10485761) is False


def test_detect_content_type():
    assert ContentType.detect("file.json") == "application/json"
    assert ContentType.detect("file.ndjson") == "application/x-ndjson"
    assert ContentType.detect("file.csv") == "text/csv"
    assert ContentType.detect("file.parquet") == "application/parquet"
    assert ContentType.detect("file.avro") == "avro/binary"
    with pytest.raises(LookupError):
        ContentType.detect("file.txt")


def test_split_posixpath_filename_dirpath():
    fullpath = "/tmp/path/to/file.txt"
    filename, dirpath = split_posixpath_filename_dirpath(fullpath)
    assert (filename, dirpath) == ("file.txt", "/tmp/path/to")
