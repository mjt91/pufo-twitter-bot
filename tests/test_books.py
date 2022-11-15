"""Test cases for the books module."""
from unittest import mock
from unittest.mock import Mock

import click
import pytest
import requests

from pufo_twitter_bot.books import randombuch


def test_buchtitelgenerator_returns_list(mock_buchtitelgenerator: Mock) -> None:
    """It returns a list."""
    books = randombuch.buchtitelgenerator()
    assert isinstance(books, list)


def test_buchtitelgenerator_returns_mocked_books(mock_buchtitelgenerator: Mock) -> None:
    """The 'Foo' book is part of books."""
    books = randombuch.buchtitelgenerator()
    assert "Foo" in books


def test_buchtitelgenerator_returns_list_of_strs(mock_buchtitelgenerator: Mock) -> None:
    """Each book is of type str."""
    books = randombuch.buchtitelgenerator()
    for book in books:
        assert isinstance(book, str)


@mock.patch("requests.get")
def test_buchtitelgenerator_raises(mock_get: Mock) -> None:
    """It rasies a ClickException when something bad happens."""
    mock_get.side_effect = requests.RequestException
    with pytest.raises(click.ClickException):
        randombuch.buchtitelgenerator()


def test_buchtitel_generator() -> None:
    """Books is a non-empty list."""
    books = randombuch.buchtitelgenerator()
    assert not (len(books) == 0)
