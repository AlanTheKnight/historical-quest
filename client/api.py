import requests
import toml

from .types import Quest

config = toml.load("config.toml")

BASE_URL = config["API"]["BASE_URL"]


async def get_quests_list() -> list[Quest]:
    data = requests.get(BASE_URL + "api/quests/", {"hidden": "false"})
    data = list(map(lambda x: Quest(**x), data.json()))
    return data
