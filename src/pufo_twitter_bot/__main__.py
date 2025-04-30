"""Command-line interface."""

from pathlib import Path

import click
from dotenv import load_dotenv

import pufo_twitter_bot
from pufo_twitter_bot.authors import opendatanames
from pufo_twitter_bot.bot.twitter import TwitterBot
from pufo_twitter_bot.books.chatgpt_generator import ChatGPTGenerator

FIRST_NAMES: Path = Path(pufo_twitter_bot.__file__).parent / "data/first-names.json"
LAST_NAMES: Path = Path(pufo_twitter_bot.__file__).parent / "data/last-names.txt"

load_dotenv()


@click.command()
@click.option(
    "-c",
    "--count",
    default=5,
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
    "--tweet/--no-tweet",
    default=False,
    help="List should be tweeted.",
    metavar="TWEET",
)
@click.version_option()
def main(count: int, gender: str, tweet: bool) -> None:
    """Pufo Twitter Bot."""
    author_list = opendatanames.random_authors(
        count=count,
        gender=gender,
        first_names_json_path=FIRST_NAMES,
        last_names_text_path=LAST_NAMES,
    )

    # Use ChatGPT to generate book-author pairs
    generator = ChatGPTGenerator()
    # Generate 5 random book-author pairs
    books = generator.generate_pairs(count=count)
    book_list = [book.title for book in books]

    for i, author in enumerate(author_list.authors):
        book = book_list[i]
        entry = f"{i + 1}. {book!r} von {author.firstname} {author.lastname}"
        click.echo(entry)
        if tweet:
            if i == 0:
                tweet_txt: str = "PUFO Bestseller Liste:\n" + entry + "\n"
            else:
                tweet_txt += entry + "\n"

    if tweet:
        # set up twitter bot instance
        twb = TwitterBot(tweet_txt)

        # tweet status update
        twb.send()


if __name__ == "__main__":
    main(prog_name="pufo-twitter-bot")  # pragma: no cover
