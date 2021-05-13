"""The twitter functionalities of pufo-twitter-bot."""
import logging
import os
from typing import Optional
from typing import Tuple

import click
import tweepy  # type: ignore
from tweepy.api import API  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def retrieve_keys() -> Tuple[
    Optional[str], Optional[str], Optional[str], Optional[str]
]:
    """Helper function to retrieve the OS environment variables.

    Returns:
        Tuple[str]: Returns the environments variables (can be None type)
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    return consumer_key, consumer_secret, access_token, access_token_secret


def create_api() -> API:
    """Creates the tweepy API object.

    Raises:
        ClickException: raises an exception if it fails to get the ENV tokens.

    Returns:
        API: Returns tweepy API object.
    """
    consumer_key, consumer_secret, access_token, access_token_secret = retrieve_keys()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except tweepy.error.TweepError as error:
        message = str(error)
        raise click.ClickException(message)
    click.echo("tweepy api created")
    return api


def validate_tweet(tweet: str) -> bool:
    """It validates the tweet.

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
