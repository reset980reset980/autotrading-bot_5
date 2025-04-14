import json

def get_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)
