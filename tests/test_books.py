"""Test cases for the books module."""

from unittest import mock
from unittest.mock import Mock

import click
import pytest
import requests  # type: ignore

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


@mock.patch("pufo_twitter_bot.books.chatgpt_generator.load_env")
@mock.patch.dict("os.environ", {}, clear=True)
def test_chatgpt_generator_initialization(mock_load_env: Mock) -> None:
    """Test ChatGPT generator can be initialized with API key."""
    from pufo_twitter_bot.books.chatgpt_generator import ChatGPTGenerator

    with pytest.raises(ValueError, match="OpenAI API key is required"):
        ChatGPTGenerator(api_key=None)


@mock.patch("pufo_twitter_bot.books.chatgpt_generator.openai.chat.completions.create")
def test_chatgpt_generator_generates_pairs(mock_openai_create: Mock) -> None:
    """Test ChatGPT generator returns list of books."""
    from pufo_twitter_bot.books.chatgpt_generator import ChatGPTGenerator

    # Mock the OpenAI response
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[
        0
    ].message.content = '{"books": [{"title": "Test Book", "author": "Test Author"}]}'
    mock_openai_create.return_value = mock_response

    generator = ChatGPTGenerator(api_key="test-key")
    books = generator.generate_pairs(count=1)

    assert len(books) == 1
    assert books[0].title == "Test Book"
    assert books[0].author.name == "Test Author"
