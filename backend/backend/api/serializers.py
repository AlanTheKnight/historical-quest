from rest_framework import serializers

from .models import Quest, Step, Option, Ending, QuestLike


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ["step"]


class StepSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Step
        fields = "__all__"


class EndingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ending
        exclude = "quest"


class CompactQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = [
            "id",
            "title",
            "description",
            "cover",
            "hidden",
            "likes",
        ]


class QuestSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)
    endings = EndingSerializer(many=True)

    class Meta:
        model = Quest
        fields = ["id", "title", "description", "cover", "hidden", "likes", "initial_step", "steps", "endings"]


class ToggleQuestLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestLike
        fields = ["telegram_id"]
        read_only_fields = ["id"]
