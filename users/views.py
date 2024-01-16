from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserScores
from .serializers import UserScoresSerializer


ERROR_MISSING_USER_ID = {"error": "User ID is required for GET request."}
ERROR_INVALID_REQUEST_DATA = {"error": "Invalid request data."}
ERROR_USER_NOT_FOUND = {"error": "User not found."}
VALID_CATEGORIES = [
    "gain",
    "general",
    "probability",
    "geometry",
    "physics",
    "other",
]
ERROR_INVALID_CATEGORY = {"error": "Invalid category."}


class UserScoresAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if not user_id:
            return Response(ERROR_MISSING_USER_ID, status=status.HTTP_400_BAD_REQUEST)

        user_math_scores = self.get_user_scores(user_id)
        if user_math_scores:
            category = request.query_params.get("category")
            return self.get_category_score_response(user_math_scores, category)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = UserScoresSerializer(data=request.data)
        return self.handle_serializer_response(serializer, status.HTTP_201_CREATED)

    def get_user_scores(self, user_id):
        try:
            return UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

    def get_category_score_response(self, user_math_scores, category):
        serializer = UserScoresSerializer(user_math_scores)
        scores_data = serializer.data

        if category and category in scores_data:
            return Response(scores_data[category], status=status.HTTP_200_OK)
        else:
            return Response(ERROR_INVALID_CATEGORY, status=status.HTTP_400_BAD_REQUEST)

    def handle_serializer_response(self, serializer, success_status):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=success_status)
        return Response(ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST)


class UserScoresUpdateAPIView(APIView):
    def patch(self, request):
        (
            user_id,
            category,
            correct_questions,
            average_difficulty,
        ) = self.get_patch_parameters(request.data)

        if (
            not user_id
            or not category
            or correct_questions is None
            or average_difficulty is None
        ):
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )

        user_math_scores = self.get_user_scores(user_id)
        if user_math_scores:
            return self.update_category_score(
                user_math_scores, category, correct_questions, average_difficulty
            )
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def get_patch_parameters(self, request_data):
        return (
            request_data.get("user_id", None),
            request_data.get("category", None),
            request_data.get("correct_questions", None),
            request_data.get("average_difficulty", None),
        )

    def update_category_score(
        self, user_math_scores, category, correct_questions, average_difficulty
    ):
        if category in VALID_CATEGORIES:
            current_score = getattr(user_math_scores, category)
            new_score = self.calculate_new_score(
                current_score, correct_questions, average_difficulty
            )
            setattr(user_math_scores, category, new_score)
            user_math_scores.save()
            return Response(
                {"message": f"Category {category} updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )

    def get_user_scores(self, user_id):
        try:
            return UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

    def calculate_new_score(self, current_score, correct_questions, average_difficulty):
        # Implement your scoring calculation logic here
        # This is a placeholder implementation, replace it with your actual logic
        return float(current_score) + (
            float(correct_questions) * float(average_difficulty)
        )
