"""Test cases for the bot module."""
import os
from unittest.mock import Mock
import tweepy  # type: ignore

import pytest

from pufo_twitter_bot.bot import twitter


def test_twitter_api(mock_tweepy_api: Mock) -> None:
    """It succeeds to update the status."""
    mock_tweepy_api.update_status("Hello Tweepy")


def test_retrieve_keys(mock_environ_variables: Mock) -> None:
    """It succeeds to retrives the keys."""
    ck, cs, at, ats = twitter.retrieve_keys()
    assert ck == "consumer_test_key"
    assert cs == "consumer_test_secret_Key"
    assert at == "access_test_token"
    assert ats == "access_test_token_secret"


def test_retrieve_keys_with_none(mock_environ_variables: Mock) -> None:
    """It returns the variables even if one is of None type."""
    # Remove mocked consumer key from environ
    del os.environ["CONSUMER_KEY"]
    ck, _, _, _ = twitter.retrieve_keys()
    assert ck is None


import click
def test_create_api_fails(mock_environ_variables: Mock) -> None:
    """It raises an error when one environment variable is missing."""
    del os.environ["CONSUMER_KEY"]
    click.ClickException
    # with pytest.raises(tweepy.error.TweepError):
    with pytest.raises(click.ClickException):
        twitter.create_api()
