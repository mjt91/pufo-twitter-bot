"""Random book titles generator."""
from typing import List

import click
import requests
from bs4 import BeautifulSoup


BOOK_URL = "https://www.buchtitelgenerator.de/"


def get_booklist_from_html() -> List[str]:
    """Retrieve a list of 5 random books from URL

    Raises:
        TypeError: If it fails to retrieve the books.

    Returns:
        List[str]: list with 5 strings with book titles
    """
    try:
        with requests.get(BOOK_URL) as response:
            response.raise_for_status()
            content = response.content

            soup = BeautifulSoup(content, "html.parser")
            books = soup.find_all("div", class_="panel-heading")

            return [book.text.strip() for book in books]

    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)


if __name__ == "__main__":
    books = get_booklist_from_html()
    print(books)
