"""Test cases for the books module."""
from typing import List

from pufo_twitter_bot.books import randombuch


def test_buchtitelgenerator_returns_list() -> None:
    books = randombuch.buchtitelgenerator()
    assert isinstance(books, list)


def test_buchtitelgenerator_returns_list_of_strs() -> None:
    books = randombuch.buchtitelgenerator()
    for book in books:
        assert isinstance(book, str)
