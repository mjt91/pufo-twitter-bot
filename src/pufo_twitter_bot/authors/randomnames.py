"""Client for the randomname.de REST API, version 1."""

from dataclasses import dataclass

import click
import requests


API_URL: str = "https://randomname.de/?format=json&count={count}&gender={gender}"


def random_authors(count: int = 10, gender: str = "a"):
    """Return a author set of size n."""

    if count <= 0:
        raise ValueError("Count has to be greater than zero")

    if gender not in ["f", "m", "b", "a"]:
        raise ValueError("Only gender 'f', 'm', 'b', 'a' is allowed")


    url = API_URL.format(count=count, gender=gender)


    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            return data
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)
