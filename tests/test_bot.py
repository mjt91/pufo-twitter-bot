"""Test cases for the bot module."""
from unittest.mock import Mock

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
