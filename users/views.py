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

        user_scores = self.get_user_scores(user_id)
        if user_scores:
            category = request.query_params.get("category")
            if category not in VALID_CATEGORIES:
                return Response(
                    {"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST
                )
            return self.get_category_score_response(user_scores, category)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = UserScoresSerializer(data=request.data)
        return self.handle_serializer_response(serializer, status.HTTP_201_CREATED)

    def patch(self, request):
        (
            user_id,
            category,
            new_score,
        ) = self.get_patch_parameters(request.data)

        if not user_id or not category or not new_score:
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )

        user_scores = self.get_user_scores(user_id)
        if user_scores:
            return self.update_category_score(user_scores, category, new_score)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def get_user_scores(self, user_id):
        try:
            return UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

    def get_category_score_response(self, user_scores, category):
        serializer = UserScoresSerializer(user_scores)
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

    def get_patch_parameters(self, request_data):
        return (
            request_data.get("user_id", None),
            request_data.get("category", None),
            request_data.get("new_score", None),
        )

    def update_category_score(self, user_scores, category, new_score):
        if category in VALID_CATEGORIES:
            setattr(user_scores, category, new_score)
            user_scores.save()
            return Response(
                {"message": f"Category {category} updated successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )


class UserHistoryAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if not user_id:
            return Response(ERROR_MISSING_USER_ID, status=status.HTTP_400_BAD_REQUEST)

        user_scores = self.get_user_scores(user_id)
        if user_scores:
            category = request.query_params.get("category")
            if category not in VALID_CATEGORIES:
                return Response(
                    {"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST
                )
            return self.get_category_score_response(user_scores, category)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
