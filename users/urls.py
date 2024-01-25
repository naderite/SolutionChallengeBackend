from django.urls import path
from .views import UserScoresAPIView, UserHistoryAPIView, UserStatsAPIView

urlpatterns = [
    path("user/scores/", UserScoresAPIView.as_view(), name="user-scores"),
    path("user/history/", UserHistoryAPIView.as_view(), name="user-history"),
    path("user/stats/", UserStatsAPIView.as_view(), name="user-stat-score"),
]
