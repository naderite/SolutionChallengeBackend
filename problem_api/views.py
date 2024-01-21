from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .backend_logic import BackendLogic

from .serializers import QuestionSerializer

from .constants import VALID_CATEGORIES


class ProblemSearchView(APIView):
    def get(self, request):
        print("Try Melowel")
        try:
            count, category, score, history = BackendLogic.validate_params(request)

            if category not in VALID_CATEGORIES:
                return BackendLogic.invalid_category_response()

            if history < 6:
                print("entering")
                eval_problems = BackendLogic.eval_student(category, history)
                if count == 1:
                    print(type(eval_problems))
                    eval_problems = eval_problems[0]
                    print(type(eval_problems))
                    serializer = QuestionSerializer(eval_problems)
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
        except ValueError:
            return Response(
                {"error": BackendLogic.ERROR_INVALID_VALUES},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError:
            return Response(
                {"error": BackendLogic.ERROR_INVALID_PARAMS},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": BackendLogic.ERROR_INTERNAL_SERVER.format(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
