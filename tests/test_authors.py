"""Test cases for the authors module."""
import json
import random
import sys
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


def setup_test_files(test_path: Path) -> None:
    """Creates a copy of all test files in the separate test folders."""
    # read and write first-names data
    with open("./tests/data/first-names-test.json", "r") as file:
        content = file.read()
        firstnames_test_file = test_path / "first-names-test.json"
        firstnames_test_file.write_text(content)

    # read and write merged data
    with open("./tests/data/first-names-merged.csv", "r") as file:
        content = file.read()
        firstnames_merged_test_file = test_path / "first-names-merged-test.csv"
        firstnames_merged_test_file.write_text(content)

    # read and write last-names data
    with open("./tests/data/last-names-test.txt", "r") as file:
        content = file.read()
        lastnames_test_file = test_path / "last-names-test.txt"
        lastnames_test_file.write_text(content)


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


@pytest.mark.skipif(
    sys.platform.startswith("linux"), reason="parsing works different on linux"
)
def test_merge_csvs_windows(tmp_path: Path) -> None:
    """It merges the csvs correctly."""
    # set up temp path folder
    data_test_path = tmp_path / "data"
    data_test_path.mkdir()
    # set up temp vornamen files to merge
    content1 = "vorname,anzahl,geschlecht\nLisa,239,w"
    content2 = "vorname,anzahl,geschlecht\nPeter,300,m"
    vornamen_test_file_1 = data_test_path / "vornamen-test-file-1.csv"
    vornamen_test_file_1.write_text(content1)
    vornamen_test_file_2 = data_test_path / "vornamen-test-file-2.csv"
    vornamen_test_file_2.write_text(content2)

    test_out_file = data_test_path / "test-data-merged.csv"
    test_input_path = str(data_test_path) + "/"

    opendatanames.merge_csvs(out_file=test_out_file, input_path=test_input_path)

    with open(test_out_file) as test_file, open(
        "./tests/data/first-names-merged.csv", encoding="utf-8"
    ) as validation_file:
        content_merged = test_file.read()
        content_validation = validation_file.read()
        assert content_merged == content_validation


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="parsing works different on windows"
)
def test_merge_csvs_linux(tmp_path: Path) -> None:
    """It merges the csvs correctly."""
    # set up temp path folder
    data_test_path = tmp_path / "data"
    data_test_path.mkdir()
    # set up temp vornamen files to merge
    content1 = "vorname,anzahl,geschlecht\nPeter,300,m"
    content2 = "vorname,anzahl,geschlecht\nLisa,239,w"
    vornamen_test_file_1 = data_test_path / "vornamen-test-file-1.csv"
    vornamen_test_file_1.write_text(content1)
    vornamen_test_file_2 = data_test_path / "vornamen-test-file-2.csv"
    vornamen_test_file_2.write_text(content2)

    test_out_file = data_test_path / "test-data-merged.csv"
    test_input_path = str(data_test_path) + "/"

    opendatanames.merge_csvs(out_file=test_out_file, input_path=test_input_path)

    with open(test_out_file) as test_file, open(
        "./tests/data/first-names-merged.csv", encoding="utf-8"
    ) as validation_file:
        content_merged = test_file.read()
        content_validation = validation_file.read()
        assert content_merged == content_validation


def test_create_first_names_data(tmp_path: Path) -> None:
    """It creates the first names dict correctly."""
    # set up temp path folder
    data_test_path = tmp_path / "data"
    data_test_path.mkdir()
    # set up temp vornamen files to test
    content_merged_names = (
        "vorname,anzahl,geschlecht\nPeter,300,m\nLisa,239,w\nLisa,100,w\n"
    )
    # write conent to files
    vornamen_merged_file = data_test_path / "first-names-merged.csv"
    vornamen_merged_file.write_text(content_merged_names)
    vornamen_test_file = data_test_path / "first-names-test.json"
    # vornamen_test_file.write_text(content_fnames)
    # run the create function
    opendatanames.create_first_names_data(
        input_file=vornamen_merged_file, out_file=vornamen_test_file
    )

    with open(vornamen_test_file, "r") as test_file, open(
        "./tests/data/first-names-test.json"
    ) as validation_file:
        content_created = json.load(test_file)
        content_validation = json.load(validation_file)

        assert content_created == content_validation
