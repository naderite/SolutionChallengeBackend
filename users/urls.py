from django.urls import path
from .views import UserScoresAPIView, UserHistoryAPIView, UserStatsAPIview

urlpatterns = [
    path("user/scores/", UserScoresAPIView.as_view(), name="user-scores"),
    path("user/history/", UserHistoryAPIView.as_view(), name="user-history"),
    path("user/stats/scores/", UserStatsAPIview.as_view(), name="user-stat-score"),
    path(
        "user/stats/history/",
        UserStatsAPIview.as_view({"get": "get_history"}),
        name="user-stat-history",
    ),
]
