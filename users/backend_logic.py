from .models import UserScores
from .serializers import UserScoresSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import (
    ERROR_INVALID_CATEGORY,
    ERROR_INVALID_REQUEST_DATA,
    VALID_SCORE_CATEGORIES,
)


class BackendLogic:
    @staticmethod
    def get_user_scores(user_id):
        try:
            return UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

    @staticmethod
    def get_category_score_response(user_scores, category):
        serializer = UserScoresSerializer(user_scores)
        scores_data = serializer.data
        if category and category in scores_data:
            return Response(scores_data[category], status=status.HTTP_200_OK)
        else:
            return Response(ERROR_INVALID_CATEGORY, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def handle_serializer_response(serializer, success_status):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=success_status)
        return Response(ERROR_INVALID_REQUEST_DATA, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_score_patch_parameters(request_data):
        return (
            request_data.get("user_id", None),
            request_data.get("category", None),
            request_data.get("new_score", None),
        )

    @staticmethod
    def get_history_patch_parameters(request_data):
        return (
            request_data.get("user_id", None),
            request_data.get("category", None),
            request_data.get("new_history", None),
        )

    @staticmethod
    def update_category_value(user_scores, category, new_score):
        setattr(user_scores, category, new_score)
        user_scores.save()
        return Response(
            {"message": f"Category {category} updated successfully."},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def get_user_scores_response(user_id):
        try:
            user = UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

        serializer = UserScoresSerializer(user)
        scores_data = serializer.data

        response_data = {
            "gain": scores_data["gain"],
            "general": scores_data["general"],
            "probability": scores_data["probability"],
            "geometry": scores_data["geometry"],
            "physics": scores_data["physics"],
            "other": scores_data["other"],
        }

        return Response(response_data)

    @staticmethod
    def get_total_history_response(user_id):
        try:
            user = UserScores.objects.get(uid=user_id)
        except UserScores.DoesNotExist:
            return None

        serializer = UserScoresSerializer(user)
        scores_data = serializer.data

        total_scores_data = {
            "total_gain": scores_data["total_gain"],
            "total_general": scores_data["total_general"],
            "total_probability": scores_data["total_probability"],
            "total_geometry": scores_data["total_geometry"],
            "total_physics": scores_data["total_physics"],
            "total_other": scores_data["total_other"],
        }

        return Response(total_scores_data)
