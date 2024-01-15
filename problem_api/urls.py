from django.urls import path
from .views import ProblemSearchView

urlpatterns = [
    path("problem-search/", ProblemSearchView.as_view(), name="problem-search-view"),
]
