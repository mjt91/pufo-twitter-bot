from __future__ import unicode_literals

import tweepy   # type: ignore
from tweepy.api import API   # type: ignore
import click

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def create_api() -> API:
    """Creates the tweepy API object.

    Raises:
        click.ClickException: raises an exception if it fails to get the ENV tokens.

    Returns:
        API: Returns tweepy API object.
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except KeyError as error:
        message = str(error)
        raise click.ClickException(message)
    click.echo("tweepy api created")
    return api


def validate_tweet() -> None:
    """Validates the tweet."""
    pass


if __name__ == "__main__":
    # Create API object
    api = create_api()
    
    # Create a tweet
    # api.update_status("Hello Tweepy")
