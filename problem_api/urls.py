from django.urls import path
from . import views

urlpatterns = [
    path(
        "get-problems-by-score/",
        views.get_problems_by_score,
        name="get_problems_by_score",
    ),
    path("get-problems-by-id/", views.get_problems_by_id, name="get_problems_by_id"),
]
