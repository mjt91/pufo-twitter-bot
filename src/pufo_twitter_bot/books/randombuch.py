"""Random book titles generator."""
from bs4 import BeautifulSoup
import requests


BOOK_URL = "https://www.buchtitelgenerator.de/"

def get_book_html():
    r = requests.get(BOOK_URL)

    content = r.content

    soup = BeautifulSoup(content)

    print(soup.prettify)