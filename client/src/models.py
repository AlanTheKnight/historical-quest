from aiogram.utils.markdown import hbold, hitalic


class Option:
    def __init__(
        self, id: int, text: str, next_step: int | None, after_text: str, after_cover: str, points: int
    ) -> None:
        self.id = id
        self.text = text
        self.next_step = next_step
        self.after_text = after_text
        self.points = points
        self.after_cover = after_cover

    def __str__(self) -> str:
        return f"Option[id={self.id}]"


class Ending:
    def __init__(self, id: int, cover: str, text: str, condition: str, **kwargs):
        self.id = id
        self.cover = cover
        self.text = text
        self.condition = condition


class Step:
    def __init__(self, id: int, title: str, text: str, cover: str, options: dict, quest: int, **kwargs) -> None:
        self.id = id
        self.title = title
        self.text = text
        self.cover = cover
        self.options = [Option(**i) for i in options]
        self.quest = quest

    def __str__(self) -> str:
        return f"Step[id={self.id}]"


class StepsManager:
    def __init__(self, steps: list[Step]):
        self._data = {step.id: step for step in steps}

    def get(self, id: int) -> Step | None:
        return self._data.get(id)


class Quest:
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        cover: str | None,
        hidden: bool,
        likes: int,
        **kwargs,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.cover = cover
        self.hidden = hidden
        self.likes = likes
        self.steps = StepsManager([Step(**i) for i in kwargs.get("steps", [])])
        self.endings = [Ending(**i) for i in kwargs.get("endings", [])]
        self.initial_step: int = kwargs.get("initial_step", None)

    def get_quest_info(self):
        return f"{hbold(self.title)}\n\n{self.description}\n\nЛайки: {self.likes}"
