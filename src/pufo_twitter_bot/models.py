from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class Author(BaseModel):
    """Pydantic model for an author."""

    name: str = Field(description="The author's full name")
    birth_date: Optional[datetime] = Field(
        None, description="The author's date of birth"
    )
    death_date: Optional[datetime] = Field(
        None, description="The author's date of death"
    )
    nationality: Optional[str] = Field(None, description="The author's nationality")
    biography: Optional[str] = Field(
        None, description="A brief biography of the author"
    )
    books: List["Book"] = Field(
        default_factory=list, description="List of books written by the author"
    )


class Book(BaseModel):
    """Pydantic model for a book."""

    title: str = Field(description="The title of the book")
    author: Author = Field(description="The author of the book")
    publication_date: Optional[datetime] = Field(
        None, description="The date the book was published"
    )
    isbn: Optional[str] = Field(None, description="The ISBN of the book")
    genre: Optional[str] = Field(None, description="The genre of the book")
    description: Optional[str] = Field(
        None, description="A brief description of the book"
    )
    page_count: Optional[int] = Field(
        None, description="The number of pages in the book"
    )


# Update forward references
Author.model_rebuild()
Book.model_rebuild()
