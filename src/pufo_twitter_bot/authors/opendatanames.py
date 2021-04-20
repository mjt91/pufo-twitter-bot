"""Script to parse the fallback data from offenedaten-koeln.de, version 1."""
from pathlib import Path
import pickle


DATAPATH: str = "../../../data/Vornamen_Koeln_{year}.csv"


def create_first_names_data():
    """Helper function to create the data from all Vornamen files.
    """

    for year in range(2010, 2011):
        fpath = Path(DATAPATH.format(year=year))
        names_dict = {}
        with open(fpath) as f:
            for i, line in enumerate(f):
                (name, gender) = line.split(",")[0], line.split(",")[2]
                names_dict[i] = [name, gender]

        with open('../../../data/first-names.pkl', 'wb') as file:
            pickle.dump(names_dict, file)


if __name__ == "__main__":
    create_first_names_data()
    print("DONE")
    with open('../../../data/first-names.pkl', 'rb') as file:
        print("READ FILE:")
        print(pickle.load(file))
