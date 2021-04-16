"""Client for the randomname.de REST API, version 1."""
from dataclasses import dataclass
from typing import List

import click
import desert
import marshmallow
import requests


@dataclass
class Author:
    """Author Ressource.

    Attributes:
        firstname: Firstname of the author.
        lastname: Surname of the author.
    """

    firstname: str
    lastname: str


@dataclass
class Ensemble:
    """Author Ensemble Ressource.

    Attributes:
        authors: A list of authors from the author ressource.

    """
    authors: List[Author]


schema = desert.schema(Ensemble, meta={"unknown": marshmallow.EXCLUDE})


API_URL: str = "https://randomname.de/?format=json&count={count}&gender={gender}"


def random_authors(count: int = 10, gender: str = "a") -> List[Author]:
    """Return a author set of size n."""

    url = API_URL.format(count=count, gender=gender)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()

            return schema.load({"authors": data})
           

    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
