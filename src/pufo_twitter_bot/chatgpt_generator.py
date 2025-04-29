"""Module for generating random authors and books using ChatGPT API."""

import os
from typing import List, Literal
import openai
from dataclasses import dataclass
import json
import logging

from .config import load_env
from .models import Book, Author

logger = logging.getLogger(__name__)

# Supported languages
Language = Literal["DE", "EN", "FR", "ES", "IT"]


@dataclass
class BookAuthorPair:
    """Data class to hold a book title and author pair."""

    title: str
    author: str


class ChatGPTGenerator:
    """Class to handle ChatGPT API interactions for generating random books and authors."""

    def __init__(self, api_key: str = None):
        """Initialize the ChatGPT generator.

        Args:
            api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY environment variable.
        """
        # Load environment variables
        load_env()

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to the constructor."
            )

        openai.api_key = self.api_key
        self.model = "gpt-4.1-nano-2025-04-14"  # Using the latest model

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the ChatGPT API."""
        return """You are a creative book title and author name generator.
        Generate unique and interesting book titles in German and matching author names.
        The book titles should be creative and memorable.
        The author names should be realistic German names.
        Format your response as a JSON array of objects with 'title' and 'author' fields."""

    def _get_user_prompt(self, count: int = 5) -> str:
        """Get the user prompt for the ChatGPT API.

        Args:
            count: Number of book-author pairs to generate.
        """
        return f"""Generate {count} random German book titles and matching author names.
        Return the response as a JSON array of objects with 'title' and 'author' fields.
        Make sure that the key in the JSON is 'books' and not 'book' or anything else.
        Example format:
        [
            {{"title": "Der Schatten des Windes", "author": "Carlos Ruiz Zafón"}},
            {{"title": "Die Vermessung der Welt", "author": "Daniel Kehlmann"}}
        ]"""

    def generate_pairs(self, count: int = 5) -> List[BookAuthorPair]:
        """Generate random book-author pairs using ChatGPT.

        Args:
            count: Number of pairs to generate.

        Returns:
            List of BookAuthorPair objects.
        """
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": self._get_user_prompt(count)},
                ],
                temperature=0.7,  # Add some randomness
                max_tokens=1000,
                response_format={"type": "json_object"},  # Ensure JSON response
            )

            # Parse the response
            content = response.choices[0].message.content
            data = json.loads(content)

            # Convert to BookAuthorPair objects
            pairs = [
                BookAuthorPair(title=item["title"], author=item["author"])
                for item in data["books"]
            ]

            # Convert to Book objects
            books = [
                Book(title=pair.title, author=Author(name=pair.author))
                for pair in pairs
            ]

            return books

        except Exception as e:
            logger.error(f"Error generating book-author pairs: {str(e)}")
            raise

    def save_to_file(self, books: List[Book], filepath: str = "generated_pairs.json"):
        """Save generated pairs to a JSON file.

        Args:
            pairs: List of BookAuthorPair objects to save
            filepath: Path to save the JSON file
        """
        data = [{"title": book.title, "author": book.author.name} for book in books]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
