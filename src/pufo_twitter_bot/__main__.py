"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Pufo Twitter Bot."""


if __name__ == "__main__":
    main(prog_name="pufo-twitter-bot")  # pragma: no cover
