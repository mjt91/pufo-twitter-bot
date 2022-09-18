"""The twitter functionalities of pufo-twitter-bot."""
from __future__ import annotations

import os
from typing import Any

import click
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
        self.api = self.create_api()

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

        return self

    def create_api(self) -> API:
        """Creates the tweepy API object.

        Raises:
            ClickException: raises an exception if it fails to get the ENV tokens.

        Returns:
            API: Returns tweepy API object.
        """
        # Get all API keys from ENV variables
        self._retrieve_keys()

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except tweepy.error.TweepError as error:
            message = str(error)
            raise click.ClickException(message) from error
        click.echo("tweepy api created")
        return api

    def send(self) -> None:
        """Tweet functionality of TwitterBot."""
        self.api.update_status(self.tweet)


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
