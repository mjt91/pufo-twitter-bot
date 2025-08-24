from datetime import datetime
from typing import Dict, Any
import pytest
from pufo_twitter_bot.models import Author, Book


@pytest.fixture
def sample_author_data() -> Dict[str, Any]:
    return {
        "name": "John Doe",
        "birth_date": datetime(1980, 1, 1),
        "nationality": "American",
        "biography": "A prolific writer",
    }


@pytest.fixture
def sample_book_data(sample_author_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title": "The Great Novel",
        "author": sample_author_data,
        "publication_date": datetime(2020, 1, 1),
        "isbn": "978-3-16-148410-0",
        "genre": "Fiction",
        "description": "A captivating story",
        "page_count": 300,
    }


def test_author_creation(sample_author_data: Dict[str, Any]) -> None:
    """Test creating an Author instance with valid data."""
    author = Author(**sample_author_data)
    assert author.name == sample_author_data["name"]
    assert author.birth_date == sample_author_data["birth_date"]
    assert author.nationality == sample_author_data["nationality"]
    assert author.biography == sample_author_data["biography"]
    assert isinstance(author.books, list)
    assert len(author.books) == 0


def test_author_required_fields() -> None:
    """Test that Author requires the name field."""
    with pytest.raises(ValueError):
        Author()  # type: ignore[call-arg]


def test_author_optional_fields() -> None:
    """Test that Author works with only required fields."""
    author = Author(name="Jane Doe")
    assert author.name == "Jane Doe"
    assert author.birth_date is None
    assert author.death_date is None
    assert author.nationality is None
    assert author.biography is None


def test_book_creation(sample_book_data: Dict[str, Any]) -> None:
    """Test creating a Book instance with valid data."""
    book = Book(**sample_book_data)
    assert book.title == sample_book_data["title"]
    assert book.author.name == sample_book_data["author"]["name"]
    assert book.publication_date == sample_book_data["publication_date"]
    assert book.isbn == sample_book_data["isbn"]
    assert book.genre == sample_book_data["genre"]
    assert book.description == sample_book_data["description"]
    assert book.page_count == sample_book_data["page_count"]


def test_book_required_fields(sample_author_data: Dict[str, Any]) -> None:
    """Test that Book requires title and author fields."""
    with pytest.raises(ValueError):
        Book()  # type: ignore[call-arg]

    with pytest.raises(ValueError):
        Book(title="The Great Novel")  # type: ignore[call-arg]

    author = Author(**sample_author_data)
    with pytest.raises(ValueError):
        Book(author=author)  # type: ignore[call-arg]


def test_book_optional_fields(sample_author_data: Dict[str, Any]) -> None:
    """Test that Book works with only required fields."""
    author = Author(**sample_author_data)
    book = Book(title="The Great Novel", author=author)
    assert book.title == "The Great Novel"
    assert book.author.name == sample_author_data["name"]
    assert book.publication_date is None
    assert book.isbn is None
    assert book.genre is None
    assert book.description is None
    assert book.page_count is None


def test_author_book_relationship(
    sample_author_data: Dict[str, Any], sample_book_data: Dict[str, Any]
) -> None:
    """Test the relationship between Author and Book models."""
    author = Author(**sample_author_data)
    book = Book(**sample_book_data)

    # Add book to author's books list
    author.books.append(book)

    assert len(author.books) == 1
    assert author.books[0].title == book.title
    assert author.books[0].author.name == author.name


def test_invalid_data_types() -> None:
    """Test that invalid data types raise appropriate errors."""
    with pytest.raises(ValueError):
        Author(name=123)  # type: ignore[arg-type]  # name should be string

    with pytest.raises(ValueError):
        Book(title=123, author=Author(name="John Doe"))  # type: ignore[arg-type]  # title should be string

    with pytest.raises(ValueError):
        Book(
            title="The Great Novel",
            author="John Doe",  # type: ignore[arg-type]  # author should be Author instance
        )
