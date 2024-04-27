"""Test cases for the authors module."""

import json
import random
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import Mock

import click
import desert
import pytest

from pufo_twitter_bot.authors import opendatanames
from pufo_twitter_bot.authors import randomnames
from pufo_twitter_bot.authors.randomnames import Author
from pufo_twitter_bot.authors.randomnames import AuthorList


def test_author_ressource_valid() -> None:
    """It loads the correct Author schema."""
    data = {"firstname": "Alice", "lastname": "Wonderland"}

    schema = desert.schema(Author)
    author = schema.load(data)

    assert author == Author(firstname="Alice", lastname="Wonderland")


def test_authors_ensemble_ressource_valid() -> None:
    """It loads the correct AuthorList schema."""
    data = {
        "authors": [
            {"firstname": "Alice", "lastname": "Wonderland", "age": 28},
            {"firstname": "Bob", "lastname": "Builder", "age": 28},
        ]
    }

    # Create a schema for the Car class.
    schema = desert.schema(AuthorList)

    # Load the data.
    ensemble = schema.load(data)
    assert ensemble == AuthorList(
        authors=[
            Author(firstname="Alice", lastname="Wonderland"),
            Author(firstname="Bob", lastname="Builder"),
        ]
    )


def test_authorlist_iter() -> None:
    """The AuthorList object is an Iterator."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert isinstance(iter(author_list), Iterator)


def test_authorlist_next() -> None:
    """It tests if AuthorList object is iterable."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert next(author_list) == Author("Lorem", "Ipsum")


def test_authorlistiterator_init() -> None:
    """The AuthorListIterator has an constructor."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert hasattr(author_list, "__iter__")


def test_authorlistiterator_has_next() -> None:
    """The AuthorListIterator has __next__ method."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    assert hasattr(author_list, "__next__")


def test_authorlistiter_stops() -> None:
    """It stops after the last Author."""
    author_list = AuthorList(authors=[Author("Lorem", "Ipsum")])
    _ = next(author_list)
    with pytest.raises(StopIteration):
        next(author_list)


class TestRandomNames:
    """Collection of all test cases for the randomname.de API."""

    def test_random_authors_returns_ensemble(self, mock_requests_get: Mock) -> None:
        """It returns a ensemble of authors."""
        authors = randomnames.random_authors()
        assert isinstance(authors, AuthorList)

    def test_random_page_handles_validation_errors(
        self, mock_requests_get: Mock
    ) -> None:
        """It raises `ClickException` when validation fails."""
        mock_requests_get.return_value.__enter__.return_value.json.return_value = None
        with pytest.raises(click.ClickException):
            randomnames.random_authors()


def setup_test_files(test_path: Path, merged_file: bool = True) -> None:
    """Creates a copy of all test files in the separate test folders."""
    # write first-names input data (two files)
    content1 = "vorname,anzahl,geschlecht\nPeter,300,m\n"
    vornamen_test_file_1 = test_path / "vornamen-test-file-1.csv"
    vornamen_test_file_1.write_text(content1, encoding="utf-8")

    content2 = "vorname,anzahl,geschlecht\nLisa,239,w\n"
    vornamen_test_file_2 = test_path / "vornamen-test-file-2.csv"
    vornamen_test_file_2.write_text(content2, encoding="utf-8")

    # read and write first-names data
    with open("./tests/data/first-names-test.json", "r", encoding="utf-8") as file:
        content = file.read()
        firstnames_test_file = test_path / "first-names-test.json"
        firstnames_test_file.write_text(content, encoding="utf-8")

    if merged_file:
        # read and write merged data
        with open("./tests/data/first-names-merged.csv", "r", encoding="utf-8") as file:
            content = file.read()
            firstnames_merged_test_file = test_path / "first-names-merged-test.csv"
            firstnames_merged_test_file.write_text(content, encoding="utf-8")

    # read and write last-names data
    with open("./tests/data/last-names-test.txt", "r", encoding="utf-8") as file:
        content = file.read()
        lastnames_test_file = test_path / "last-names-test.txt"
        lastnames_test_file.write_text(content, encoding="utf-8")


def test_random_authors_fallback(tmp_path: Path) -> None:
    """The test authors are generated from the fallback file."""
    # setup test files
    setup_test_files(tmp_path)
    # set random seed to ensure testability
    random.seed(2)

    first_names_test_json = str(tmp_path / "first-names-test.json")
    last_names_text_path_test_path = str(tmp_path / "last-names-test.txt")

    author_list = opendatanames.random_authors(
        first_names_json_path=first_names_test_json,
        last_names_text_path=last_names_text_path_test_path,
        count=2,
    )
    result_list = [
        Author(firstname="Peter", lastname="Lorem"),
        Author(firstname="Lisa", lastname="Ipsum"),
    ]

    assert result_list == author_list.authors


def test_random_authors_fallback_gender_m() -> None:
    """It returns only the male authors."""
    author_list = opendatanames.random_authors(
        first_names_json_path="./tests/data/first-names-test.json",
        last_names_text_path="./tests/data/last-names-test.txt",
        count=1,
        gender="m",
    )

    assert author_list.authors[0].firstname == "Peter"


def test_random_authors_fallback_gender_w() -> None:
    """It returns only the female authors."""
    author_list = opendatanames.random_authors(
        first_names_json_path="./tests/data/first-names-test.json",
        last_names_text_path="./tests/data/last-names-test.txt",
        count=1,
        gender="w",
    )

    assert author_list.authors[0].firstname == "Lisa"


def test_random_authors_fallback_fails_with_unknown_gender() -> None:
    """It fails to get the authors."""
    with pytest.raises(ValueError):
        opendatanames.random_authors(
            first_names_json_path="./tests/data/first-names-test.json",
            last_names_text_path="./tests/data/last-names-test.txt",
            gender="r",
        )


def test_merge_csvs_windows(tmp_path: Path) -> None:
    """It merges the csvs correctly."""
    setup_test_files(tmp_path, merged_file=False)

    test_out_file = tmp_path / "test-data-merged-2.csv"
    test_input_path = tmp_path

    opendatanames.merge_csvs(out_file=test_out_file, input_path=test_input_path)

    test_validation_file = Path("./tests/data/first-names-merged.csv")

    with open(test_out_file, encoding="utf-8") as test_file, open(
        test_validation_file, encoding="utf-8"
    ) as validation_file:
        content_merged = test_file.read()
        content_validation = validation_file.read()
        assert content_merged == content_validation


def test_create_first_names_data(tmp_path: Path) -> None:
    """It creates the first names dict correctly."""
    # setup test files
    setup_test_files(tmp_path)

    # write conent to input file
    vornamen_merged_file = tmp_path / "first-names-merged-test.csv"
    with open(vornamen_merged_file, "a") as test_file:
        test_file.write("Peter,123,m\n")

    # define outfile
    vornamen_test_out_file = tmp_path / "first-names-test-2.json"

    # validation file path
    validation_test_file = tmp_path / "first-names-test.json"

    # run the create function
    opendatanames.create_first_names_data(
        input_file=vornamen_merged_file, out_file=str(vornamen_test_out_file)
    )

    with open(vornamen_test_out_file, "r") as test_file, open(
        validation_test_file
    ) as validation_file:
        content_created = json.load(test_file)
        content_validation = json.load(validation_file)

        assert content_created == content_validation
