import os
from pathlib import Path
import json

# with open("fcc.json", "r") as fcc_file:
#     fcc_data = json.load(fcc_file)
#     print(fcc_data)


def travese_folder(full_path):
    for dirpath, dirnames, filenames in os.walk(full_path):
        return filenames


DATA_DIR = (
    f"{Path(__file__).resolve().parent.parent.parent.parent.parent}/data/"
)


if __name__ == "__main__":
    print(travese_folder(DATA_DIR))
