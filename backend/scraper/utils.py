import json
import os.path


def load_auth():
    path_file = os.path.join("scraper", "auth.json")

    with open(path_file, "r") as file:
        return json.load(file)
