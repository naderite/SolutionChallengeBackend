from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from .backend_logic import BackendLogic
from .constants import (
    ERROR_INVALID_REQUEST_DATA,
    ERROR_MISSING_USER_ID,
    ERROR_USER_NOT_FOUND,
    VALID_SCORE_CATEGORIES,
    VALID_HISTORY_CATEGORIES,
    ERROR_MISSING_DATA_TYPE,
    ERROR_INVALID_DATA_TYPE,
)
from .serializers import UserScoresSerializer

import logging

logger = logging.getLogger(__name__)


class UserScoresAPIView(APIView):
    def get(self, request):
        logger.info("in get")
        user_id = request.query_params.get("user_id", None)
        try:
            if not user_id:
                raise ValueError(ERROR_MISSING_USER_ID)

            user_scores = BackendLogic.get_user_scores(user_id)

            if not user_scores:
                raise ValueError(ERROR_USER_NOT_FOUND)

            category = request.query_params.get("category")
            if category not in VALID_SCORE_CATEGORIES:
                raise ValueError("Invalid category.")

            return BackendLogic.get_category_score_response(user_scores, category)

        except ValueError as ve:
            logger.error(str(ve))
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        logger.error(str(request.data))
        serializer = UserScoresSerializer(data=request.data)
        return BackendLogic.handle_serializer_response(
            serializer, status.HTTP_201_CREATED
        )

    def patch(self, request):
        try:
            logger.info("in patch")
            user_id, category, new_score = BackendLogic.get_score_patch_parameters(
                request.data
            )

            if not user_id or not category or not new_score:
                raise ValueError(ERROR_INVALID_REQUEST_DATA)

            user_scores = BackendLogic.get_user_scores(user_id)

            if not user_scores:
                raise ValueError(ERROR_USER_NOT_FOUND)
            if category not in VALID_SCORE_CATEGORIES:
                raise ValueError("Invalid score category.")
            return BackendLogic.update_category_value(user_scores, category, new_score)

        except ValueError as ve:
            logger.error(str(ve))
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserHistoryAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)

        try:
            if not user_id:
                raise ValueError(ERROR_MISSING_USER_ID)

            user_history = BackendLogic.get_user_scores(user_id)

            if not user_history:
                raise ValueError(ERROR_USER_NOT_FOUND)

            category = request.query_params.get("category")
            if category not in VALID_HISTORY_CATEGORIES:
                raise ValueError("Invalid history category.")

            return BackendLogic.get_category_score_response(user_history, category)

        except ValueError as ve:
            logger.error(str(ve))
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        try:
            user_id, category, new_history = BackendLogic.get_history_patch_parameters(
                request.data
            )

            if not user_id or not category or not new_history:
                raise ValueError(ERROR_INVALID_REQUEST_DATA)

            user_history = BackendLogic.get_user_scores(user_id)

            if not user_history:
                raise ValueError(ERROR_USER_NOT_FOUND)
            if category not in VALID_HISTORY_CATEGORIES:
                raise ValueError("Invalid history category.")
            return BackendLogic.update_category_value(
                user_history, category, new_history
            )

        except ValueError as ve:
            logger.error(str(ve))
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(str(e))
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserStatsAPIView(APIView):
    def get(self, request):
        user_id = request.query_params.get("user_id", None)
        data = request.query_params.get("type", None)
        try:
            if not user_id:
                raise ValueError(ERROR_MISSING_USER_ID)
            elif not data:
                raise ValueError(ERROR_MISSING_DATA_TYPE)
            if data == "score":
                return BackendLogic.get_user_scores_response(user_id)
            elif data == "history":
                return BackendLogic.get_total_history_response(user_id)
            elif data == "favorites":
                return BackendLogic.get_favorites(user_id)
            elif data == "recent":
                return BackendLogic.get_recent(user_id)
            else:
                # Log the unexpected data value
                logger.warning("Unexpected data value: %s", data)
                return Response(
                    {"error": ERROR_INVALID_DATA_TYPE},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError as ve:
            # Log the ValueError
            logger.error(str(ve))
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log other exceptions
            logger.exception("An unexpected error occurred")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
