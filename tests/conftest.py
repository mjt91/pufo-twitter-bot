"""Package-wide test fixtures."""
from unittest.mock import Mock
import os

import pytest
import tweepy  # type: ignore
from _pytest.config import Config
from pytest_mock import MockFixture


def pytest_configure(config: Config) -> None:
    """Pytest configuration hook."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    """Fixture for mocking requests.get."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = [
        {
            "firstname": "Peter",
            "lastname": "Lorem",
        },
        {
            "firstname": "Lisa",
            "lastname": "Ipsum",
        },
    ]
    return mock


@pytest.fixture
def mock_randomnames_random_authors(mocker: MockFixture) -> Mock:
    """Fixture for mocking authors.randomname.random_authors."""
    return mocker.patch("pufo_twitter_bot.authors.randomnames.random_authors")


@pytest.fixture
def mock_tweepy_api(mocker: MockFixture) -> Mock:
    """Fixture for mocking tweepy.api object."""
    return mocker.patch.object(tweepy, "API", autospec=True)


@pytest.fixture
def mock_environ_variables(mocker: MockFixture) -> Mock:
    """Fixture for mocking the environment variables for twitter api."""
    return mocker.patch.dict(
        os.environ, {
            "consumer_key": "consumer_test_key",
            "consumer_secret": "consumer_test_secret_Key",
            "access_token": "access_test_token", 
            "access_token_secret": "access_test_token_secret"
    })
    
