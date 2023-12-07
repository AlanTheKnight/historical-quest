from django.db import models
from django_jsonform.models.fields import JSONField
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize


class Option(models.Model):
    """Модель варианта ответа на шаге квеста."""

    text = models.TextField(verbose_name="Текст")
    next_step = models.ForeignKey(
        "Step",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
        related_name="next_step",
        verbose_name="Следующий шаг",
    )
    after_text = models.TextField(verbose_name="Текст после ответа", blank=True)
    after_cover = ProcessedImageField(
        upload_to="covers",
        format="PNG",
        options={"quality": 60},
        processors=[
            SmartResize(1080, 720, upscale=False),
        ],
        blank=True,
    )

    step = models.ForeignKey("Step", on_delete=models.CASCADE, related_name="options", verbose_name="Шаг")

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"


class Step(models.Model):
    """Модель шага квеста."""

    title = models.CharField(max_length=200)
    text = models.TextField()
    cover = models.ImageField(upload_to="covers", blank=True)
    quest = models.ForeignKey("Quest", on_delete=models.CASCADE, related_name="steps", verbose_name="Квест")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Шаг"
        verbose_name_plural = "Шаги"


class Quest(models.Model):
    """Модель квеста."""

    SCHEMA = {"type": "array", "items": {"type": "string"}}

    title = models.CharField(max_length=200, verbose_name="Название", unique=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    initial_step = models.ForeignKey(
        "Step",
        on_delete=models.PROTECT,
        related_name="initial_step",
        blank=True,
        null=True,
        default=None,
        verbose_name="Начальный шаг",
    )
    sum_rules = JSONField(
        schema=SCHEMA,
        blank=True,
        null=True,
        default=None,
        verbose_name="Результирующие правила",
    )
    cover = ProcessedImageField(
        upload_to="covers",
        format="PNG",
        options={"quality": 60},
        processors=[
            SmartResize(1080, 720, upscale=False),
        ],
        blank=True,
    )

    hidden = models.BooleanField(default=True, verbose_name="Скрытый")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(initial_step__isnull=True) & models.Q(hidden=True) | models.Q(initial_step__isnull=False)
                ),
                name="Условия показа квеста (указан начальный шаг)",
            )
        ]

    @property
    def completed_stats(self):
        return CompletedStats.objects.filter(quest=self, finished_at__isnull=False).count()

    @property
    def likes(self):
        return QuestLike.objects.filter(quest=self).count()


class CompletedStats(models.Model):
    """Статистика прохождения квестов пользователями."""

    telegram_id = models.IntegerField(verbose_name="Telegram ID пользователя")
    quest = models.ForeignKey("Quest", on_delete=models.CASCADE, verbose_name="Квест")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Начат")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершен")

    def __str__(self) -> str:
        return f"{self.telegram_id} - {self.quest}"

    class Meta:
        verbose_name = "Прохождения"
        verbose_name_plural = "Прохождения"


class QuestLike(models.Model):
    """Лайки квестов пользователями."""

    telegram_id = models.IntegerField(verbose_name="Telegram ID пользователя")
    quest = models.ForeignKey("Quest", on_delete=models.CASCADE, verbose_name="Квест")

    def __str__(self) -> str:
        return f"{self.telegram_id} - {self.quest}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        unique_together = ("telegram_id", "quest")
