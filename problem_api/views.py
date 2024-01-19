from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .serializers import QuestionSerializer

from django.http import Http404

import random


class ProblemSearchView(APIView):
    def get(self, request):
        print("Try Melowel")
        try:
            print("Try thenya")
            # Validate and parse input parameters
            
            try:
                print("Try in views1")
                count = int(request.query_params.get("count"))
                category1 = request.query_params.get("category")
                score = int(request.query_params.get("score"))
                print("Affecta")
                print(count)
                print(category1)
                print(score)
            except ValueError:
                return Response(
                    {
                        "error": "Invalid count or score. Please provide valid numeric values."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except TypeError:
                return Response(
                    {
                        "error": "Missing or invalid query parameters. Please provide count, category, and score."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Fetch questions based on the given difficulty score and category
            problems = Question.objects.filter(
                category=category1, difficulty_score=score
            )
            if count == 1:
                try:
                    # Try to get a random question from the filtered queryset
                    selected_problem = problems.order_by("?").first()
                    if selected_problem is None:
                        raise Http404(
                            "No question found with the specified difficulty score"
                        )
                except Http404:
                    tolerance = 1
                    while selected_problem is None:
                        # Try to find a question with score + tolerance or score - tolerance
                        problems = Question.objects.filter(
                            category=category1,
                            difficulty_score__in=[score + tolerance, score - tolerance],
                        )
                        selected_problem = problems.order_by("?").first()
                        tolerance += 1
                serializer = QuestionSerializer(selected_problem)
                return Response(serializer.data)
            else:
                # Fetch additional problems with harder scores
                tolerance = 1
                remaining = count - problems.count()
                while problems.count() < remaining // 2:
                    additional_problems = Question.objects.filter(
                        category=category1, difficulty_score=score + tolerance
                    )
                    problems = problems.union(additional_problems)
                    tolerance += 1

                # Fetch additional problems with easier scores
                tolerance = 1
                while problems.count() < count:
                    additional_problems = Question.objects.filter(
                        category=category1, difficulty_score=score - tolerance
                    )
                    problems = problems.union(additional_problems)
                    tolerance += 1
        except Exception as e:
            return Response(
                {"error": f"Internal server error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)
