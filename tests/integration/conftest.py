import random
import string

import pytest

from crux import Crux


class Helpers:
    @staticmethod
    def generate_random_string(length):
        char_set = string.ascii_uppercase + string.digits
        return "".join(random.sample(char_set * length, length))


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture(scope="module")
def connection():
    return Crux()


@pytest.fixture(scope="session")
def dataset():
    conn = Crux()
    char_set = string.ascii_uppercase + string.digits
    dataset_name = "crux_py_dataset_" + "".join(random.sample(char_set * 6, 6))
    dataset = conn.create_dataset(name=dataset_name, description="test_description")
    yield dataset
    dataset.delete()


@pytest.fixture(scope="session")
def dataset_with_crux_domain():
    conn = Crux(only_use_crux_domains=True)
    char_set = string.ascii_uppercase + string.digits
    dataset_name = "crux_py_dataset_" + "".join(random.sample(char_set * 6, 6))
    dataset = conn.create_dataset(name=dataset_name, description="test_description")
    yield dataset
    dataset.delete()
