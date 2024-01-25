from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import BackendLogic

from .serializers import QuestionSerializer

from .constants import VALID_CATEGORIES


class ProblemSearchView(APIView):
    def get(self, request):
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
                eval_problems = BackendLogic.eval_student(category)
                if count == 1:
                    raise ValueError("Invalid request: new and count cannot both be 1.")
                else:
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
            return Response(
                {"error": f"ValueError: {str(ve)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError as te:
            return Response(
                {"error": f"TypeError: {str(te)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": BackendLogic.ERROR_INTERNAL_SERVER.format(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
