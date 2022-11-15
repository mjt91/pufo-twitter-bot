"""Random book titles generator from the buchtitelgenerator.de page."""
from typing import List

import click
import requests
from bs4 import BeautifulSoup  # type: ignore


# BOOK_URL = "https://www.buchtitelgenerator.de/"
BOOK_URL = "https://buchtitelgenerator.de/generator/"


def buchtitelgenerator() -> List[str]:
    """Retrieve a list of 5 random books from URL.

    Raises:
        ClickException: shows the error if it fails to retrieve the books.

    Returns:
        List[str]: list with 5 strings with book titles.
    """
    try:
        with requests.get(BOOK_URL) as response:
            response.raise_for_status()
            content = response.content

            soup = BeautifulSoup(content, "html.parser")

            # As of November 2022 the site got slight changes that now
            # returns a list of paragraphs, the two last ones are empty HTML p-tags
            container = soup.find("div", class_="entry clr")
            paragraphs = container.find_all("p")
            # Only first five entries
            books = [book.text for book in paragraphs[:5]]

            return [book.strip() for book in books]

    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message) from error
