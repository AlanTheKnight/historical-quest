from rest_framework import serializers

from .models import Quest, Step, Option, CompletedStats, QuestLike


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ["step"]


class StepSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Step
        fields = "__all__"


class CompactQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = [
            "id",
            "title",
            "description",
            "cover",
            "hidden",
            # "completed_stats",
            "likes",
        ]


class QuestSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True)

    class Meta:
        model = Quest
        fields = [
            "id",
            "title",
            "description",
            "cover",
            "hidden",
            # "completed_stats",
            "likes",
            "initial_step",
            "steps",
            "sum_rules",
        ]


class CompletedStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedStats
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class ToggleQuestLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestLike
        fields = ["telegram_id"]
        read_only_fields = ["id"]
