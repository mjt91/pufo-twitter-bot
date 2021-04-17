"""Test cases for the authors module."""
from unittest.mock import Mock

import click
import desert
import pytest

from pufo_twitter_bot.authors import randomnames
from pufo_twitter_bot.authors.randomnames import Author
from pufo_twitter_bot.authors.randomnames import AuthorList


def test_random_authors_returns_ensemble(mock_requests_get: Mock) -> None:
    """It returns a ensemble of authors."""
    authors = randomnames.random_authors()
    assert isinstance(authors, AuthorList)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """It raises `ClickException` when validation fails."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        randomnames.random_authors()


def test_author_ressource_valid() -> None:
    """It loads the correct Author schema."""
    data = {"firstname": "Alice", "lastname": "Wonderland"}

    schema = desert.schema(Author)
    author = schema.load(data)

    assert author == Author(firstname="Alice", lastname="Wonderland")


def test_authors_ensemble_ressource_valid() -> None:
    """It loads the correct AuthorList schema."""
    data = {
        "authors": [
            {"firstname": "Alice", "lastname": "Wonderland", "age": 28},
            {"firstname": "Bob", "lastname": "Builder", "age": 28},
        ]
    }

    # Create a schema for the Car class.
    schema = desert.schema(AuthorList)

    # Load the data.
    ensemble = schema.load(data)
    assert ensemble == AuthorList(
        authors=[
            Author(firstname="Alice", lastname="Wonderland"),
            Author(firstname="Bob", lastname="Builder"),
        ]
    )
