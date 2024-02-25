from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from .backend_logic import BackendLogic

from rest_framework.decorators import api_view
from .serializers import QuestionSerializer

from .constants import VALID_CATEGORIES

import logging

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_problems_by_score(request):
    try:
        try:
            count, category, score, new = BackendLogic.validate_params(request)
        except ValueError and TypeError:
            return Response(
                {"error": "Invalid or missing parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if category not in VALID_CATEGORIES:
            return BackendLogic.invalid_category_response()

        if new == 1:
            assert count != 1, "Invalid request: new and count cannot both be 1."
            eval_problems = BackendLogic.eval_student(category)
            serializer = QuestionSerializer(eval_problems, many=True)
            return Response(serializer.data)

        problems = BackendLogic.get_filtered_problems(category, score)

        if count == 1:
            selected_problem = BackendLogic.get_single_problem(
                problems, category, score
            )
            serializer = QuestionSerializer(selected_problem)
            return Response(serializer.data)
        else:
            selected_problems = BackendLogic.get_multiple_problems(
                problems, count, category, score
            )
            serializer = QuestionSerializer(selected_problems, many=True)
            return Response(serializer.data)

    except Http404 as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        logger.error(str(ve))

        return Response(
            {"error": f"ValueError: {str(ve)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except TypeError as te:
        logger.error(str(te))

        return Response(
            {"error": f"TypeError: {str(te)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except AssertionError as ae:
        logger.error(str(ae))
        return Response(
            {"error": f"TypeError: {str(ae)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(str(e))

        return Response(
            {"error": BackendLogic.ERROR_INTERNAL_SERVER.format(str(e))},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
def get_problems_by_id(request):
    try:
        ids = request.GET.getlist("ids")
        problems = BackendLogic.filter_problems_by_ids(ids)
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)
    except Http404 as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as ve:
        logger.error(str(ve))

        return Response(
            {"error": f"ValueError: {str(ve)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except TypeError as te:
        logger.error(str(te))
        return Response(
            {"error": f"TypeError: {str(te)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(str(e))
        return Response(
            {"error": BackendLogic.ERROR_INTERNAL_SERVER.format(str(e))},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
