import pytest

from crux._utils import (
    Headers,
    quote,
    split_posixpath_filename_dirpath,
    str_to_bool,
    url_builder,
    valid_chunk_size,
)
from crux.models.resource import MediaType


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


def test_detect_media_type():
    assert MediaType.detect("file.json") == "application/json"
    assert MediaType.detect("file.ndjson") == "application/x-ndjson"
    assert MediaType.detect("file.csv") == "text/csv"
    assert MediaType.detect("file.parquet") == "application/parquet"
    assert MediaType.detect("file.avro") == "avro/binary"
    with pytest.raises(LookupError):
        MediaType.detect("file.txt")


def test_split_posixpath_filename_dirpath():
    fullpath = "/tmp/path/to/file.txt"
    filename, dirpath = split_posixpath_filename_dirpath(fullpath)
    assert (filename, dirpath) == ("file.txt", "/tmp/path/to")


def test_str_to_bool():
    assert str_to_bool("True") is True
    assert str_to_bool("true") is True
    assert str_to_bool("False") is False
    assert str_to_bool("false") is False

    with pytest.raises(ValueError):
        assert str_to_bool("crux")


def test_headers():
    header = Headers({"Header-Key": "HeaderValue"})
    assert header == {"header-key": "HeaderValue"}
    header["Header-Key-2"] = "HeaderValue2"
    assert header == {"header-key": "HeaderValue", "header-key-2": "HeaderValue2"}
    header.update({"Header-Key-3": "HeaderValue3"})
    assert header == {
        "header-key": "HeaderValue",
        "header-key-2": "HeaderValue2",
        "header-key-3": "HeaderValue3",
    }
    header.update({"Header-Key": "ChangedHeaderValue"})
    assert header == {
        "header-key": "ChangedHeaderValue",
        "header-key-2": "HeaderValue2",
        "header-key-3": "HeaderValue3",
    }

    assert header.get("Header-Key") == "ChangedHeaderValue"
    assert header.get("HeAdEr-KeY") == "ChangedHeaderValue"
    assert header.get("header-key") == "ChangedHeaderValue"
    assert header.get("HEADER-KEY") == "ChangedHeaderValue"

    assert header["Header-Key"] == "ChangedHeaderValue"
    assert header["HeAdEr-KeY"] == "ChangedHeaderValue"
    assert header["header-key"] == "ChangedHeaderValue"
    assert header["HEADER-KEY"] == "ChangedHeaderValue"
