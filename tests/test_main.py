"""Test cases for the __main__ module."""

import random
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pufo_twitter_bot import __main__


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@patch("pufo_twitter_bot.__main__.FIRST_NAMES", "tests/data/first-names-test.json")
@patch("pufo_twitter_bot.__main__.LAST_NAMES", "tests/data/last-names-test.txt")
def test_main_prints_authors(runner: CliRunner) -> None:
    """It prints the names of the fallback authors."""
    random.seed(2)  # use seed to guarantee testability
    result = runner.invoke(__main__.main, ["--count", "2"])
    assert "Peter Lorem" in result.output and "Lisa Ipsum" in result.output
