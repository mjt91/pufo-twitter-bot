"""Command-line interface."""
import click

from .authors.randomnames import random_authors


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
    author_set = random_authors(count=count, gender=gender)
    click.echo(author_set)


if __name__ == "__main__":
    main(prog_name="pufo-twitter-bot")  # pragma: no cover
