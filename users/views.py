from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .backend_logic import BackendLogic

from .constants import (
    ERROR_INVALID_REQUEST_DATA,
    ERROR_MISSING_USER_ID,
    ERROR_USER_NOT_FOUND,
    VALID_SCORE_CATEGORIES,
    VALID_HISTORY_CATEGORIES,
)

from .serializers import UserScoresSerializer


class UserScoresAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if not user_id:
            return Response(ERROR_MISSING_USER_ID, status=status.HTTP_400_BAD_REQUEST)

        user_scores = BackendLogic.get_user_scores(user_id)
        if user_scores:
            category = request.query_params.get("category")
            if category not in VALID_SCORE_CATEGORIES:
                return Response(
                    {"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST
                )
            return BackendLogic.get_category_score_response(user_scores, category)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = UserScoresSerializer(data=request.data)
        return BackendLogic.handle_serializer_response(
            serializer, status.HTTP_201_CREATED
        )

    def patch(self, request):
        (
            user_id,
            category,
            new_score,
        ) = BackendLogic.get_score_patch_parameters(request.data)

        if not user_id or not category or not new_score:
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )

        user_scores = BackendLogic.get_user_scores(user_id)
        if user_scores:
            return BackendLogic.update_category_score(user_scores, category, new_score)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)


class UserHistoryAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        if not user_id:
            return Response(ERROR_MISSING_USER_ID, status=status.HTTP_400_BAD_REQUEST)

        user_history = BackendLogic.get_user_scores(user_id)
        if user_history:
            category = request.query_params.get("category")
            if category not in VALID_HISTORY_CATEGORIES:
                return Response(
                    {"error": "Invalid category."}, status=status.HTTP_400_BAD_REQUEST
                )
            return BackendLogic.get_category_score_response(user_history, category)
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        (
            user_id,
            category,
            new_history,
        ) = BackendLogic.get_history_patch_parameters(request.data)

        if not user_id or not category or not new_history:
            return Response(
                ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST
            )

        user_history = BackendLogic.get_user_scores(user_id)
        if user_history:
            return BackendLogic.update_category_score(
                user_history, category, new_history
            )
        else:
            return Response(ERROR_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
