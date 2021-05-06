"""Test cases for the bot module."""


def test_twitter_api(mock_tweepy_api):
    # tw = mocker.patch.object(tweepy, "API", autospec=True)
    mock_tweepy_api.update_status("Hello Tweepy")
