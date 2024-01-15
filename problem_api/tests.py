from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Question
from .serializers import QuestionSerializer


class ProblemSearchViewTests(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        self.client = APIClient()
        # Create a sample Question for testing
        self.sample_question1 = Question.objects.create(
            problem="Sample Problem",
            rationale="Sample Rationale",
            options="Option A, Option B, Option C, Option D",
            correct="A",
            annotated_formula="Sample Annotated Formula",
            linear_formula="Sample Linear Formula",
            category="Sample Category",
            difficulty_score=2,
        )
        self.sample_question2 = Question.objects.create(
            problem="Sample Problem",
            rationale="Sample Rationale",
            options="Option A, Option B, Option C, Option D",
            correct="A",
            annotated_formula="Sample Annotated Formula",
            linear_formula="Sample Linear Formula",
            category="Sample Category",
            difficulty_score=3,
        )
        self.sample_question3 = Question.objects.create(
            problem="Sample Problem",
            rationale="Sample Rationale",
            options="Option A, Option B, Option C, Option D",
            correct="A",
            annotated_formula="Sample Annotated Formula",
            linear_formula="Sample Linear Formula",
            category="Sample Category",
            difficulty_score=3,
        )

    def test_single_problem_view(self):
        # Test the API view for fetching a single problem
        expected_data = {
            "id": self.sample_question1.id,
            "problem": "Sample Problem",
            "rationale": "Sample Rationale",
            "options": "Option A, Option B, Option C, Option D",
            "correct": "A",
            "annotated_formula": "Sample Annotated Formula",
            "linear_formula": "Sample Linear Formula",
            "category": "Sample Category",
            "difficulty_score": 2,
        }

        url = reverse("problem-search-view")
        response = self.client.get(
            url, {"count": 1, "category": "Sample Category", "score": 2}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}. Response content: {response.content}",
        )

        # Sort the dictionaries based on keys
        response_data_sorted = dict(sorted(response.data.items()))
        expected_data_sorted = dict(sorted(expected_data.items()))

        self.assertEqual(response_data_sorted, expected_data_sorted)

    def test_multiple_problems_view(self):
        expected_data = [
            {
                "id": self.sample_question1.id,
                "problem": "Sample Problem",
                "rationale": "Sample Rationale",
                "options": "Option A, Option B, Option C, Option D",
                "correct": "A",
                "annotated_formula": "Sample Annotated Formula",
                "linear_formula": "Sample Linear Formula",
                "category": "Sample Category",
                "difficulty_score": 2,
            },
            {
                "id": self.sample_question2.id,
                "problem": "Sample Problem",
                "rationale": "Sample Rationale",
                "options": "Option A, Option B, Option C, Option D",
                "correct": "A",
                "annotated_formula": "Sample Annotated Formula",
                "linear_formula": "Sample Linear Formula",
                "category": "Sample Category",
                "difficulty_score": 3,
            },
            {
                "id": self.sample_question3.id,
                "problem": "Sample Problem",
                "rationale": "Sample Rationale",
                "options": "Option A, Option B, Option C, Option D",
                "correct": "A",
                "annotated_formula": "Sample Annotated Formula",
                "linear_formula": "Sample Linear Formula",
                "category": "Sample Category",
                "difficulty_score": 3,
            },
        ]
        # Test the API view for fetching multiple problems
        url = reverse("problem-search-view")
        response = self.client.get(
            url, {"count": 3, "category": "Sample Category", "score": 3}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}. Response content: {response.content}",
        )

        expected_data_sorted = sorted(expected_data, key=lambda x: x["id"])
        actual_data_sorted = sorted(response.data, key=lambda x: x["id"])
        self.assertEqual(actual_data_sorted, expected_data_sorted)
