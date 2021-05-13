"""The twitter functionalities of pufo-twitter-bot."""
import logging
import os
from typing import Tuple

import click
import tweepy  # type: ignore
from tweepy.api import API  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def retrieve_keys() -> Tuple[str, str, str, str]:
    """Helper function to retrieve the OS environment variables.

    Raises:
        OSError: If any environment variable is not set.

    Returns:
        [type]: [description]
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    env_var_list = [consumer_key, consumer_secret, access_token, access_token_secret]

    if any(var is None for var in env_var_list):
        raise OSError("Environment variables not set.")

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
    except KeyError as error:
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
        raise ValueError("tweet is more than 280 unicode characters")
    else:
        return True


if __name__ == "__main__":
    # Create API object
    api = create_api()

    # Create a tweet
    # api.update_status("Hello Tweepy")
