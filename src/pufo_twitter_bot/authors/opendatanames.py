"""Script to parse the fallback data from offenedaten-koeln.de, version 1."""
import csv
import glob
import json
import os
import random
from pathlib import Path

import desert
import marshmallow

from pufo_twitter_bot.authors.randomnames import Author
from pufo_twitter_bot.authors.randomnames import AuthorList


DATAPATH: str = "../../../data/first-names-merged.csv"


def merge_csvs():
    """Helper function to merge all  offenedaten-köln csv files into one."""
    csv_list = glob.glob("../../../data/*.csv")

    # get fieldnames
    with open(csv_list[0], newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames

    # merge
    result_name = "../../../data/first-names-merged.csv"

    with open(result_name, "w+", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in csv_list:
            with open(file, newline="") as theread:
                reader = csv.DictReader(theread)
                for row in reader:
                    writer.writerow(row)


def create_first_names_data():
    """Helper function to create the data from all Vornamen files."""
    # load data from file path
    fpath = Path(DATAPATH)

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

    with open("../../../data/first-names.json", "w", encoding="utf-8") as file:
        json.dump(names_dict, file, ensure_ascii=False, indent=2)


AuthorSchema = desert.schema_class(Author, meta={"unknown": marshmallow.EXCLUDE})()
AuthorListSchema = desert.schema(AuthorList, meta={"unknown": marshmallow.EXCLUDE})


def random_authors(count: int = 10, gender: str = "a"):
    """Return a author set of size n.

    Args:
        count (int): Decides the size of the returned set. Defaults to 10.
        gender (str): Decides which gender names should be returned from the
            'data json files'. Possible options are:
            w - generate only female names
            m - generate only male names

    Returns:
        AuthorList: A nested List of List[Author] (dataclass).
    """
    with open("../../../data/first-names.json", "r") as file:
        first_names = json.load(file)
        rnd_sample_keys = random.sample(list(first_names.keys()), count)

        first_names_list = []
        for key in rnd_sample_keys:
            fnames_dict = {"firstname": first_names[key][0], "lastname": "Mustermann"}
            first_names_list.append(fnames_dict)

        return AuthorListSchema.load({"authors": first_names_list})


if __name__ == "__main__":

    csv_files = [os.path.basename(x) for x in glob.glob("../../../data/*.csv")]
    json_files = [os.path.basename(x) for x in glob.glob("../../../data/*.json")]

    if "first-names-merged.csv" not in csv_files:
        print("Created merged csv file with all first names")
        merge_csvs()

    if "first-names.json" not in json_files:
        print("Created json file with unique names")
        create_first_names_data()

    random_authors()
