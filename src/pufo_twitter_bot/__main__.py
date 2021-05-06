"""Command-line interface."""
import click

from .authors import opendatanames
from .authors import randomnames
from .books import randombuch
from .bot import twitter

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
@click.option(
    "-s",
    "--source",
    default="randomname",
    type=click.Choice(["randomname", "offenedaten"], case_sensitive=False),
    metavar="SOURCE",
    help="Set the source of the authors names.",
)
@click.option(
    "--tweet/--no-tweet",
    default=False,
    help="List should be tweeted.",
    metavar="TWEET",
)
@click.version_option()
def main(count: int, gender: str, source: str, tweet: bool) -> None:
    """Pufo Twitter Bot."""
    if source == "randomname":
        author_list = randomnames.random_authors(
            count=count,
            gender=gender,
        )
    if source == "offenedaten":
        author_list = opendatanames.random_authors(
            count=count,
            gender=gender,
            first_names_json_path=FIRST_NAMES,
            last_names_text_path=LAST_NAMES,
        )

    book_list = randombuch.buchtitelgenerator()

    if count > 5:
        run_num = round(count / 5)
        for _ in range(0, run_num):
            new_books = randombuch.buchtitelgenerator()
            book_list += new_books

    for i, author in enumerate(author_list.authors):
        book = book_list[i]
        entry = f"{i+1}. '{book}' von {author.firstname} {author.lastname}"
        click.echo(entry)
        if tweet:
            if i == 0:
                tweet = "PUFO Bestseller Liste:\n" + entry + "\n"
            else:
                tweet += entry + "\n"
        
    print(tweet)
    print(twitter.validate_tweet(tweet))

if __name__ == "__main__":
    main(prog_name="pufo-twitter-bot")  # pragma: no cover
