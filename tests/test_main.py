"""Test cases for the __main__ module."""
from unittest.mock import Mock

import pytest
import requests
from click.testing import CliRunner

from pufo_twitter_bot import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0


def test_main_prints_authors(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints the names of the authors."""
    result = runner.invoke(__main__.main)
    assert ("Peter Lorem" in result.output and "Lisa Ipsum" in result.output)


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It invokdes requests get."""
    runner.invoke(__main__.main)
    assert mock_requests_get.called


def test_main_uses_count_and_gender(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It uses the English Wikipedia by default."""
    runner.invoke(__main__.main)
    args, _ = mock_requests_get.call_args
    assert ("10" in args[0] and "a" in args[0])


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exists with a non-zero status code if the request fails."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(__main__.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It prints an error message if the request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(__main__.main)
    assert "Error" in result.output
