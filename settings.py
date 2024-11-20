import json


def get_settings(what: list = None) -> dict:
    with open("settings/settings.json", "r") as f:
        setting = json.load(f)

    if what:

        for i in what:
            setting = setting[i]

        return setting

    return setting
