from aiogram.utils.markdown import hbold, hitalic


class Quest:
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        cover: str | None,
        sum_rules: str,
        hidden: bool,
        initial_step: str,
        **kwargs,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.sum_rules = sum_rules
        self.cover = cover
        self.hidden = hidden
        self.initial_step = initial_step

    def get_quest_info(self):
        return f"{self.id}) {self.title}\n\n{hitalic(self.description)}"
