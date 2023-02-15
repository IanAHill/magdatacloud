import pytest


pytest_plugins = [
    "magdataapp.tests.fixtures",
]


@pytest.fixture
def password():
    return "password"
