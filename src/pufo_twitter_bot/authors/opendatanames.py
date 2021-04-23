"""Script to parse the fallback data from offenedaten-koeln.de, version 1."""
import csv
import glob
import json
import os
import random
from pathlib import Path
from typing import Union

import desert
import marshmallow

from pufo_twitter_bot.authors.randomnames import Author
from pufo_twitter_bot.authors.randomnames import AuthorList


DATAPATH: str = "../../../data/"


def merge_csvs() -> None:
    """Helper function to merge all  offenedaten-köln csv files into one."""
    csv_list = glob.glob(DATAPATH + "*.csv")

    # get fieldnames
    with open(csv_list[0], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

    # merge
    result_name = DATAPATH + "first-names-merged.csv"

    with open(result_name, "w+", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)  # type: ignore
        writer.writeheader()
        for file in csv_list:
            with open(file, newline="") as theread:
                reader = csv.DictReader(theread)
                for row in reader:
                    writer.writerow(row)


def create_first_names_data() -> None:
    """Helper function to create the data from all Vornamen files."""
    # load data from file path
    fpath = Path(DATAPATH + "first-names-merged.csv")

    # create output file dict and set (for unique names)
    names_dict = {}
    unique_names = set()

    with open(fpath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                pass
            else:
                (name, gender) = (
                    line.rstrip().split(",")[0],
                    line.rstrip().split(",")[2],
                )
                if name not in unique_names:
                    names_dict[i] = [name, gender]
                    unique_names.add(name)

    with open(DATAPATH + "first-names.json", "w", encoding="utf-8") as file:
        json.dump(names_dict, file, ensure_ascii=False, indent=2)


# Load the schemas for Author and AuthorList

AuthorSchema = desert.schema_class(Author, meta={"unknown": marshmallow.EXCLUDE})()
AuthorListSchema = desert.schema(AuthorList, meta={"unknown": marshmallow.EXCLUDE})


def random_authors(
    count: int = 10,
    gender: str = "a",
    first_names_json_path: Union[str, Path] = None,
    last_names_text_path: Union[str, Path] = None,
) -> AuthorList:
    """Return a author set of size n.

    The function is using the fallback data in the data folder (on top level).
    It loads the first names from 'first-names.json' and 'last-names.txt'.

    Args:
        first_names_json_path (Union[str, Path]): path or file string to another
            first names file. Defaults to None. Will take the data files from
            the top level data folder if None.
        last_names_text_path (Union[str, Path]): path or file string to another
            last names text file. Defaults to None. Will take the data files from
            the top level data folder if None.
        count (int): Decides the size of the returned set. Defaults to 10.
        gender (str): Decides which gender names should be returned from the
            'data json files'. Possible options are:
            a - generate authors from both genders
            w - generate only female names
            m - generate only male names

    Raises:
        ValueError: the first names dict (first-names.json) gets parsed and
            filtered on the gender column. value error gets raised when gender
            is not in [a, w, m].

    Returns:
        AuthorList: A nested List of List[Author] (dataclass).
    """
    first_names_json_path = (
        first_names_json_path
        if first_names_json_path is not None
        else Path("../../../data/first-names.json")
    )
    last_names_text_path = (
        last_names_text_path
        if last_names_text_path is not None
        else Path("../../../data/last-names.txt")
    )

    with open(first_names_json_path, "r") as ffile, open(
        last_names_text_path, "r"
    ) as lfile:
        first_names = json.load(ffile)
        last_names = lfile.read().splitlines()
        rnd_sample_last_names = random.sample(last_names, count)

        if gender == "a":
            rnd_sample_keys = random.sample(list(first_names.keys()), count)
        elif gender == "w":
            first_names_w = {k: v for k, v in first_names.items() if v[1] == "w"}
            rnd_sample_keys = random.sample(list(first_names_w.keys()), count)

        elif gender == "m":
            first_names_m = {k: v for k, v in first_names.items() if v[1] == "m"}
            rnd_sample_keys = random.sample(list(first_names_m.keys()), count)

        else:
            raise ValueError("Gender must be either of 'a', 'w' or 'm'")

        first_names_list = []
        for key, last_name in zip(rnd_sample_keys, rnd_sample_last_names):
            fnames_dict = {"firstname": first_names[key][0], "lastname": last_name}
            first_names_list.append(fnames_dict)

    return AuthorListSchema.load({"authors": first_names_list})  # type: ignore


if __name__ == "__main__":

    csv_files = [os.path.basename(x) for x in glob.glob(DATAPATH + "*.csv")]
    json_files = [os.path.basename(x) for x in glob.glob(DATAPATH + "*.json")]

    if "first-names-merged.csv" not in csv_files:
        print("Created merged csv file with all first names")
        merge_csvs()

    if "first-names.json" not in json_files:
        print("Created json file with unique names")
        create_first_names_data()

    authors = random_authors()
    print(authors)
