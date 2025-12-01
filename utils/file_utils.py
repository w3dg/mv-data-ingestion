import json
import os

DATA_FOLDER = "extracted_data"
BQ_DATA_FOLDER = "bq_data"


def save_json(filename, data):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    filepath = os.path.join(DATA_FOLDER, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_json(filename):
    filepath = os.path.join(DATA_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return None
