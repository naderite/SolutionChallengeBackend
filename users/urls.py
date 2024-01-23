from django.urls import path
from .views import UserScoresAPIView, UserHistoryAPIView

urlpatterns = [
    path("user/scores/", UserScoresAPIView.as_view(), name="user-scores"),
    path("user/history/", UserHistoryAPIView.as_view(), name="user-history"),
]
