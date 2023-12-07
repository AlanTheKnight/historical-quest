from rest_framework.generics import ListAPIView, GenericAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Quest, CompletedStats, QuestLike


class QuestsListView(ListAPIView):
    serializer_class = serializers.ListQuestSerializer
    queryset = Quest.objects.all()
    filterset_fields = ["hidden"]


class QuestRetrieveView(RetrieveAPIView):
    serializer_class = serializers.QuestSerializer
    queryset = Quest.objects.all()


class CompletedStatsView(CreateAPIView):
    serializer_class = serializers.CompletedStatsSerializer
    queryset = CompletedStats.objects.all()


class CompletedStatsRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = serializers.CompletedStatsSerializer
    queryset = CompletedStats.objects.all()


class ToggleQuestLikeView(GenericAPIView):
    serializer_class = serializers.ToggleQuestLikeSerializer

    def post(self, request, *args, **kwargs):
        """Toggle like of a quest for a given Telegram ID.

        If the like already exists, delete it. Otherwise, create a new one.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telegram_id = serializer.validated_data["telegram_id"]
        quest_id = self.kwargs["quest_pk"]

        like, created = QuestLike.objects.get_or_create(
            telegram_id=telegram_id,
            quest_id=quest_id,
        )

        if not created:
            like.delete()

        return Response(status=status.HTTP_200_OK)