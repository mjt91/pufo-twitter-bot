"""Test cases for the bot module."""
from unittest.mock import Mock


def test_twitter_api(mock_tweepy_api: Mock) -> None:
    """It succeeds to update the status."""
    # tw = mocker.patch.object(tweepy, "API", autospec=True)
    mock_tweepy_api.update_status("Hello Tweepy")
