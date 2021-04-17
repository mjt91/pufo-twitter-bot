"""Random book titles generator."""

from bs4 import BeautifulSoup
import requests


BOOK_URL = "https://www.buchtitelgenerator.de/aasdasdas"

def get_booklist_from_html():
    r = requests.get(BOOK_URL)
    content = r.content

    soup = BeautifulSoup(content, 'html.parser')
    books = soup.find_all("div", class_="panel-heading")

    if books:
        return [book.text.strip() for book in books]
    else:
        raise TypeError(f"Error parsing the '{BOOK_URL}' html source")



if __name__ == "__main__":
    books = get_booklist_from_html()
    print(books)