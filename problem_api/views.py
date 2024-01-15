from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .serializers import QuestionSerializer

from django.http import Http404
from django.shortcuts import get_list_or_404

import random


class ProblemSearchView(APIView):
    def get(self, request):
        try:
            # Validate and parse input parameters
            try:
                count = int(request.query_params.get("count"))
                category = request.query_params.get("category")
                score = int(request.query_params.get("score"))
            except (ValueError, TypeError) as e:
                return Response(
                    {"error": "Invalid input parameters"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            problems = []
            if count == 1:
                try:
                    # Fetch all questions with the given difficulty score
                    problems = get_list_or_404(
                        Question, category=category, difficulty_score=score
                    )

                    # Randomly choose one question from the list
                    selected_problem = random.choice(problems)
                    problems = [selected_problem]
                except Http404:
                    tolerance = 1
                    while True:
                        try:
                            # Try to find a question with score + tolerance or score - tolerance
                            problem = get_list_or_404(
                                Question,
                                category=category,
                                difficulty_score__in=[
                                    score + tolerance,
                                    score - tolerance,
                                ],
                            )
                            selected_problem = random.choice(problems)
                            problems = [selected_problem]
                        except Http404:
                            pass  # Continue the loop if a question is not found
                        tolerance += 1
                        if len(problems) >= 1:
                            break  # Exit the loop if at least one question is found
                serializer = QuestionSerializer(selected_problem)
                return Response(serializer.data)
            else:
                # Fetch all questions with the given difficulty score
                problems = get_list_or_404(
                    Question, category=category, difficulty_score=score
                )

                # Fetch additional problems with harder scores
                tolerance = 1
                remaining = count - len(problems)
                while len(problems) < remaining // 2:
                    try:
                        # Fetch questions with score + tolerance
                        additional_problems = get_list_or_404(
                            Question,
                            category=category,
                            difficulty_score=score + tolerance,
                        )

                        # Add the fetched questions to the list
                        problems.extend(additional_problems)
                    except Http404:
                        pass  # Continue the loop if a question is not found
                    tolerance += 1

                # Fetch additional problems with easier scores
                tolerance = 1
                while len(problems) < count:
                    try:
                        # Fetch questions with score - tolerance
                        additional_problems = get_list_or_404(
                            Question,
                            category=category,
                            difficulty_score=score - tolerance,
                        )

                        # Add the fetched questions to the list
                        problems.extend(additional_problems)
                    except Http404:
                        pass  # Continue the loop if a question is not found
                    tolerance += 1
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        serializer = QuestionSerializer(problems, many=True)
        return Response(serializer.data)
