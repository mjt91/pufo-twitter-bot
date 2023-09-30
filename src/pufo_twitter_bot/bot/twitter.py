"""The twitter functionalities of pufo-twitter-bot."""
from __future__ import annotations

import os
from typing import Any

import tweepy  # type: ignore
from tweepy.api import API  # type: ignore


class TwitterBot:
    """The twitter bot class.

    This class is used to have all the twitter functionalities for
    pufo_twitter_bot package.
    """

    def __init__(self, tweet: str):
        """Constructor.

        Args:
            tweet (str): The text to tweet.
        """
        self.tweet = tweet
        self.client = self.create_client()

    @property
    def tweet(self) -> str:
        """The tweet property."""
        return self._tweet

    @tweet.setter
    def tweet(self, value: Any) -> None:
        if not isinstance(value, str):
            raise TypeError("tweet must be of type `str`.")
        self._tweet = value

    def _retrieve_keys(
        self,
    ) -> TwitterBot:
        """Helper function to retrieve the OS environment variables.

        Returns:
            TwitterBot: Returns self.
        """
        self.consumer_key = os.getenv("CONSUMER_KEY")
        self.consumer_secret = os.getenv("CONSUMER_SECRET")
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("BEARER_TOKEN")
        return self

    def create_client(self) -> API:
        """Creates the tweepy API object.

        Returns:
            API: Returns tweepy API object.
        """
        # Get all API keys from ENV variables
        self._retrieve_keys()
        client = tweepy.Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
        )

        return client

    def send(self) -> None:
        """Tweet functionality of TwitterBot."""
        self.client.create_tweet(text=self.tweet)


def validate_tweet(tweet: str) -> bool:
    """It validates a tweet.

    Args:
        tweet (str): The text to tweet.

    Raises:
        ValueError: Raises if tweet length is more than 280 unicode characters.

    Returns:
        bool: True if validation holds.
    """
    str_len = ((tweet).join(tweet)).count(tweet) + 1
    if str_len > 280:
        raise ValueError(f"tweet is more than 280 unicode characters\n {tweet}")
    else:
        return True
