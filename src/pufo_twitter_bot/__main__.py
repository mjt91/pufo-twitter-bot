"""Command-line interface."""
import click

from .authors import opendatanames
from .books import randombuch

FIRST_NAMES = "./data/first-names.json"
LAST_NAMES = "./data/last-names.txt"


@click.command()
@click.option(
    "-c",
    "--count",
    default=10,
    help="Count of the returned random names",
    metavar="COUNT",
    show_default=True,
)
@click.option(
    "-g",
    "--gender",
    default="a",
    help="Set Gender of returned names set",
    metavar="GENDER",
    show_default=True,
)
@click.version_option()
def main(count: int, gender: str) -> None:
    """Pufo Twitter Bot."""
    author_list = opendatanames.random_authors(
        count=count,
        gender=gender,
        first_names_json_path=FIRST_NAMES,
        last_names_text_path=LAST_NAMES,
    )
      
    book_list = randombuch.buchtitelgenerator()

    if count > 5:
        run_num = round(count / 5)
        for i in range(0, run_num):
            new_books = randombuch.buchtitelgenerator()
            book_list += new_books

    for i, author in enumerate(author_list.authors):
        book = book_list[i]
        click.echo(
            f"{i+1}. Platz '{book}' von {author.firstname} {author.lastname}"
        )


if __name__ == "__main__":
    main(prog_name="pufo-twitter-bot")  # pragma: no cover
