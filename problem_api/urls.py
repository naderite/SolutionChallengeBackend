from django.urls import path
from .views import ProblemSearchView

urlpatterns = [
    path("search-problem/", ProblemSearchView.as_view(), name="problem-search-view"),
]
