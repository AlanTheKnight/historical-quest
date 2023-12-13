from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers
from .models import Quest, QuestLike


class QuestsListView(ListAPIView):
    queryset = Quest.objects.all()
    filterset_fields = ["hidden", "title"]

    def get_serializer_class(self):
        if self.request.query_params.get("compact", "True").lower() == "true":
            return serializers.CompactQuestSerializer
        return serializers.QuestSerializer


class QuestRetrieveView(RetrieveAPIView):
    queryset = Quest.objects.all()

    def get_serializer_class(self):
        if self.request.query_params.get("compact", "False").lower() == "true":
            return serializers.CompactQuestSerializer
        return serializers.QuestSerializer


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
