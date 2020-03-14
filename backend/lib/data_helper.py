import json


def load_json(file):
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def save_json(data, file):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
