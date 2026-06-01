import json
import random
import os


def get_file_path():
    return os.path.join(os.path.dirname(__file__), "data.json")


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_categories(data):
    unique_categories = set()
    for item in data:
        for category in item["category"]:
            unique_categories.add(category)
    return sorted(unique_categories)


def get_random_item_by_category(data, category):
    if category == "Zufällig":
        available_items = data
    else:
        available_items = [item for item in data if category in item["category"]]
    return random.choice(available_items) if available_items else None
