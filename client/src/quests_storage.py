import time

from . import api
from .models import Quest
from typing import Dict, Optional


class QuestsStorage:
    def __init__(self) -> None:
        self._data: Optional[Dict[int, Quest]] = None

    async def _list_quests(self):
        quests = await api.get_quests_list(compact=False)
        self._data = {q.id: q for q in quests}

    def get_quest_by_title(self, title: str) -> Quest | None:
        res = list(filter(lambda q: q.title == title, self._data.values()))
        if res:
            return res[0]
        return None

    def get_quest_by_id(self, id: int) -> Quest | None:
        return self._data.get(id, None)

    async def toggle_like(self, quest_id: int, telegram_id: int) -> Quest:
        await api.toggle_like(quest_id, telegram_id)
        quest = await api.get_quest_by_id(quest_id, compact=False)
        self._data[quest_id] = quest
        return quest

    async def data(self):
        if self._data is None:
            await self._list_quests()
        return list(self._data.values())


class ResultStorage:
    def __init__(self) -> None:
        self._data = {}

    def start(self, telegram_id: int, quest_id: int) -> None:
        self._data[(telegram_id, quest_id)] = [0, []]

    def add_points(self, telegram_id: int, quest_id: int, points: int) -> None:
        self._data[(telegram_id, quest_id)][0] += points

    def complete_step(self, telegram_id: int, quest_id: int, step_id: int) -> None:
        self._data[(telegram_id, quest_id)][1].append(step_id)

    def step_done(self, telegram_id: int, quest_id: int, step_id: int) -> None:
        if (telegram_id, quest_id) not in self._data:
            return False
        return step_id in self._data[(telegram_id, quest_id)][1]

    def pop(self, telegram_id: int, quest_id: int) -> int:
        return self._data.pop((telegram_id, quest_id))
