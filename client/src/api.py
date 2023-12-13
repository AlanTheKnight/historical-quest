import requests
import toml
import enum

from .models import Quest

config = toml.load("config.toml")

BASE_URL = config["API"]["BASE_URL"]
AUTH_TOKEN = config["API"]["AUTH_TOKEN"]


class APIEndpoints(enum.Enum):
    QUESTS = BASE_URL + "quests/"
    QUEST = BASE_URL + "quests/{quest_id}/"
    QUEST_LIKE = BASE_URL + "quests/{quest_id}/like"


headers = {"Authorization": f"Token {AUTH_TOKEN}"}


async def get_quests_list(compact: bool = True) -> list[Quest]:
    data = requests.get(
        APIEndpoints.QUESTS.value,
        params={"hidden": "false", "compact": "true" if compact else "false"},
        headers=headers,
    )
    data = list(map(lambda x: Quest(**x), data.json()))
    return data


async def toggle_like(quest_id: int, telegram_id: int) -> Quest | None:
    resp = requests.post(
        APIEndpoints.QUEST_LIKE.value.format(quest_id=quest_id),
        headers=headers,
        data={"telegram_id": telegram_id},
    )
    quest = await get_quest_by_id(quest_id, compact=True)
    return quest


async def get_quest_by_id(quest_id: int, compact: bool = False) -> Quest | None:
    data = requests.get(
        APIEndpoints.QUEST.value.format(quest_id=quest_id),
        headers=headers,
        params={"compact": "true" if compact else "false"},
    )
    json = data.json()
    return None if data.status_code == 404 else Quest(**json)
