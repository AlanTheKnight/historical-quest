from django.urls import path
from . import views

urlpatterns = [
    path("quests/", views.QuestsListView.as_view()),
    path("quests/<int:pk>/", views.QuestRetrieveView.as_view()),
    path("quests/<int:quest_pk>/like", views.ToggleQuestLikeView.as_view()),
]
