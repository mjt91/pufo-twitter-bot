"""Test cases for the bot module."""
from pytest_mock import MockFixture
from pytest_mock import mocker
import os
from pufo_twitter_bot.bot import twitter

import tweepy

import pytest


def test_twitter_api(mock_tweepy_api):
    # tw = mocker.patch.object(tweepy, "API", autospec=True)
    mock_tweepy_api.update_status("Hello Tweepy")
