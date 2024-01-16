from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserScores


class UserMathScoresAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.urlget = reverse("user-scores")
        self.urlupdate = reverse("update-user-score")

    def test_get_scores_success(self):
        user_scores = UserScores.objects.create(uid="user123", gain=10, general=20)
        response = self.client.get(
            self.urlget, {"user_id": "user123", "category": "gain"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.data,
            10,
            f"Expected response data to be 10, but got {response.data}. Response content: {response.content.decode('utf-8')}",
        )

    def test_get_scores_missing_user_id(self):
        response = self.client.get(self.urlget)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"Expected status code 400, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"User ID is required for GET request."}',
            f"Expected content to be {{'error': 'User ID is required for GET request.'}}, but got {response.content.decode('utf-8')}",
        )

    def test_get_scores_user_not_found(self):
        response = self.client.get(self.urlget, {"user_id": "nonexistent"})
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status code 404, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"User not found."}',
            f"Expected content to be {{'error': 'User not found.'}}, but got {response.content.decode('utf-8')}",
        )

    def test_post_scores_success(self):
        data = {"uid": "user123", "gain": 10, "general": 20}
        response = self.client.post(self.urlget, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected status code 201, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        # Add additional assertions based on your specific implementation

    def test_post_scores_invalid_data(self):
        data = {"user_id": "user123", "invalid_field": "value"}
        response = self.client.post(self.urlget, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"Expected status code 400, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"Invalid request data."}',
            f"Expected content to be {{'error': 'Invalid request data.'}}, but got {response.content.decode('utf-8')}",
        )

    def test_patch_scores_success(self):
        user_scores = UserScores.objects.create(uid="user123", gain=10, general=20)

        data = {
            "user_id": "user123",
            "category": "gain",
            "correct_questions": 5,
            "average_difficulty": 2.0,
        }
        response = self.client.patch(self.urlupdate, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected status code 200, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        # Add additional assertions based on your specific implementation

    def test_patch_scores_invalid_data(self):
        data = {"user_id": "user123", "invalid_field": "value"}
        response = self.client.patch(self.urlupdate, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"Expected status code 400, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"Invalid request data."}',
            f"Expected content to be {{'error':'Invalid request data.'}}, but got {response.content.decode('utf-8')}",
        )

    def test_patch_scores_missing_data(self):
        data = {"user_id": "user123", "category": "gain"}
        response = self.client.patch(self.urlupdate, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"Expected status code 400, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"Invalid request data."}',
            f"Expected content to be {{'error': 'Correct questions and average difficulty are required for PATCH request.'}}, but got {response.content.decode('utf-8')}",
        )

    def test_patch_scores_user_not_found(self):
        data = {
            "user_id": "nonexistent",
            "category": "gain",
            "correct_questions": 5,
            "average_difficulty": 2.0,
        }
        response = self.client.patch(self.urlupdate, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
            f"Expected status code 404, but got {response.status_code}. Response content: {response.content.decode('utf-8')}",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error":"User not found."}',
            f"Expected content to be {{'error': 'User not found.'}}, but got {response.content.decode('utf-8')}",
        )
