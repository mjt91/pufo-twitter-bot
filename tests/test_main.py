"""Test cases for the __main__ module."""
from unittest.mock import Mock

import pytest
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
    runner.invoke(console.main)
    assert mock_requests_get.called
