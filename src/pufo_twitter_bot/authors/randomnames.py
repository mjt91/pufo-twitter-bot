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
        lastname: Lastname of the author.
    """

    firstname: str
    lastname: str


AuthorSchema = desert.schema_class(Author, meta={"unknown": marshmallow.EXCLUDE})()


@dataclass
class AuthorList:
    """AuthorList Ressource.

    Attributes:
        authors: A list of authors from the author ressource.

    """

    authors: List[Author] = desert.field(
        marshmallow_field=marshmallow.fields.List(
            marshmallow.fields.Nested(AuthorSchema)
        )
    )  # type: ignore

    def __iter__(self) -> AuthorListIterator:
        """Returns the AuthorList iterator object."""
        return AuthorListIterator(self)


class AuthorListIterator:
    """Iterator class for AuthorList."""

    def __init__(self, authorlist: AuthorList) -> None:
        """Constructor for the AuthorList iterator class.

        Create a reference for the Authors in the AuthorList object.
        Initialize the index to zero for iterator loop.

        Args:
            authorlist (AujthorList): AuthorList object reference
        """
        self._authors: List[Author] = authorlist.authors
        self._index: int = 0

    def __next__(self) -> Author:
        """Returns the next author from the AuthorList list."""
        if self._index < len(self._authors):
            result: Author = self._authors[self._index]

            self._index += 1
            return result

        raise StopIteration


AuthorListSchema = desert.schema(AuthorList, meta={"unknown": marshmallow.EXCLUDE})


API_URL: str = "https://randomname.de/?format=json&count={count}&gender={gender}"


def random_authors(count: int = 10, gender: str = "a") -> AuthorList:
    """Return a author set of size n.

    Args:
        count (int): Decides the size of the returned set. Defaults to 10.
        gender (str): Decides which gender names should be returned from the
            'randomname.de REST API'. Possible options are:
            f - generate only female names
            m - generate only male names
            b - generate both genders
            a - generate all genders (some entries have no gender assinged)

    Raises:
        ClickException: raises the error message returned from the API.

    Returns:
        AuthorList: A nested List of List[Author] (dataclass).
    """
    url = API_URL.format(count=count, gender=gender)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()

            return AuthorListSchema.load({"authors": data})  # type: ignore

    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message)
