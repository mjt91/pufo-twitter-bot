"""Test cases for the authors module."""
import os
import random
from collections.abc import Iterable
from unittest import mock
from unittest.mock import Mock

import click
import desert
import pytest

from pufo_twitter_bot.authors import opendatanames
from pufo_twitter_bot.authors import randomnames
from pufo_twitter_bot.authors.randomnames import Author
from pufo_twitter_bot.authors.randomnames import AuthorList
from pufo_twitter_bot.authors.randomnames import AuthorListIterator


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


def test_authorlist_iterable() -> None:
    """The AuthorList is of type Iterable."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert isinstance(author_list, Iterable)


def test_authorlistiterator_init() -> None:
    """The AuthorListIterator has an constructor."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert hasattr(author_list, "__iter__")


def test_authorlistiterator_has_next() -> None:
    """The AuthorListIterator has __next__ method."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    author_list_iterator = AuthorListIterator(author_list)
    assert hasattr(author_list_iterator, "__next__")


def test_authorlistiter_returns_iteratorcls() -> None:
    """Iter of AuthorList returns the iterator."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert isinstance(iter(author_list), AuthorListIterator)


def test_authorlistiter_next_returns_next_author():
    """The next method returns the next Author from AuthorList."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    author_list_iterator = iter(author_list)
    assert next(author_list_iterator) == Author("Lorem", "Ipsum")


def test_authorlistiter_stops():
    """It stops after the last Author."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    author_list_iterator = iter(author_list)
    _ = next(author_list_iterator) == Author("Lorem", "Ipsum")

    with pytest.raises(StopIteration):
        next(author_list_iterator)


def test_random_authors_fallback() -> None:
    """The test authors are generated from the fallback file."""
    # set random seed to ensure testability
    random.seed(2)

    author_list = opendatanames.random_authors(
        first_names_json_path="./tests/data/first-names-test.json",
        last_names_text_path="./tests/data/last-names-test.txt",
        count=2,
    )
    result_list = [
        Author(firstname="Lorem", lastname="Ipsum"),
        Author(firstname="Dolor", lastname="Sit-Amit"),
    ]

    assert result_list == author_list.authors


def test_random_authors_fallback_gender_m() -> None:
    """It returns only the male authors."""
    author_list = opendatanames.random_authors(
        first_names_json_path="./tests/data/first-names-test.json",
        last_names_text_path="./tests/data/last-names-test.txt",
        count=1,
        gender="m",
    )

    assert author_list.authors[0].firstname == "Lorem"


def test_random_authors_fallback_gender_w() -> None:
    """It returns only the female authors."""
    author_list = opendatanames.random_authors(
        first_names_json_path="./tests/data/first-names-test.json",
        last_names_text_path="./tests/data/last-names-test.txt",
        count=1,
        gender="w",
    )

    assert author_list.authors[0].firstname == "Dolor"


def test_random_authors_fallback_fails_with_unknown_gender() -> None:
    """It fails to get the authors."""
    with pytest.raises(ValueError):
        opendatanames.random_authors(
            first_names_json_path="./tests/data/first-names-test.json",
            last_names_text_path="./tests/data/last-names-test.txt",
            gender="r",
        )


def test_merge_csvs() -> None:
    """It merges all csvs in the input directory."""
    fname = "./tests/data/first-names-merged.csv"
    if os.path.isfile(fname):
        os.remove(fname)

    with mock.patch("pufo_twitter_bot.authors.opendatanames.DATAPATH", "./tests/data/"):
        opendatanames.merge_csvs()

    assert os.path.isfile(fname)
