# backend_logic.py
import random
from rest_framework.response import Response
from rest_framework import status

from .models import Question
from .constants import (
    EVAL_PROBLEMS_10,
    EVAL_PROBLEMS_30,
    EVAL_PROBLEMS_40,
    EVAL_PROBLEMS_60,
    EVAL_PROBLEMS_70,
    EVAL_PROBLEMS_90,
)


class BackendLogic:
    ERROR_INVALID_VALUES = (
        "Invalid count or score. Please provide valid numeric values."
    )
    ERROR_INVALID_PARAMS = "Missing or invalid query parameters. Please provide count, category, and score."
    ERROR_INVALID_CATEGORY = "Invalid category."
    ERROR_INTERNAL_SERVER = "Internal server error: {}"

    @staticmethod
    def validate_params(request):
        count = int(request.query_params.get("count"))
        category = request.query_params.get("category")
        score = int(request.query_params.get("score"))
        history = int(request.query_params.get("history"))
        return count, category, score, history

    @staticmethod
    def invalid_category_response():
        return Response(
            {"error": BackendLogic.ERROR_INVALID_CATEGORY},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def get_filtered_problems(category, score):
        return Question.objects.filter(category=category, difficulty_score=score)

    @staticmethod
    def get_single_problem(problems, category, score):
        selected_problem = problems.order_by("?").first()
        tolerance = 1
        while selected_problem is None:
            problems = Question.objects.filter(
                category=category,
                difficulty_score__in=[score + tolerance, score - tolerance],
            )
            selected_problem = problems.order_by("?").first()
            tolerance += 1
        return selected_problem

    @staticmethod
    def get_multiple_problems(problems, count, category, score):
        selected_problems = Question.objects.none()

        if problems.exists():
            all_problem_ids = list(problems.values_list("id", flat=True))

            if problems.count() > 5:
                selected_problem_ids = random.sample(
                    all_problem_ids, min(count, len(all_problem_ids))
                )

                selected_problems = Question.objects.filter(id__in=selected_problem_ids)
            else:
                selected_problems = Question.objects.filter(id__in=all_problem_ids)
                remaining = count - selected_problems.count()
                selected_problems = BackendLogic.fetch_additional_problems(
                    selected_problems, category, score, remaining // 2, 1, +1
                )
                selected_problems = BackendLogic.fetch_additional_problems(
                    selected_problems, category, score, remaining // 2, 1, -1
                )
        else:
            selected_problems = BackendLogic.fetch_additional_problems(
                selected_problems, category, score, count // 2, 1, +1
            )
            selected_problems = BackendLogic.fetch_additional_problems(
                selected_problems, category, score, count, 1, -1
            )

        return selected_problems

    @staticmethod
    def fetch_additional_problems(
        selected_problems, category, score, target_count, tolerance, direction
    ):
        additional_problems = Question.objects.filter(
            category=category, difficulty_score=score + direction * tolerance
        )

        tolerance += 1

        while additional_problems.count() < target_count:
            additional_problems = additional_problems.union(
                Question.objects.filter(
                    category=category, difficulty_score=score + direction * tolerance
                )
            )
            tolerance += 1

        selected_problems_ids = list(additional_problems.values_list("id", flat=True))[
            :target_count
        ]

        selected_problems = selected_problems.union(
            Question.objects.filter(id__in=selected_problems_ids)
        )
        return selected_problems

    @staticmethod
    def eval_student(category, history):
        id_10 = random.choice(EVAL_PROBLEMS_10[category])
        id_30 = random.choice(EVAL_PROBLEMS_30[category])
        id_40 = random.choice(EVAL_PROBLEMS_40[category])
        id_60 = random.choice(EVAL_PROBLEMS_60[category])
        id_70 = random.choice(EVAL_PROBLEMS_70[category])
        id_90 = random.choice(EVAL_PROBLEMS_90[category])

        problem_ids = [id_10, id_30, id_40, id_60, id_70, id_90]
        # Retrieve questions using the IDs
        problems = [Question.objects.get(id=id_) for id_ in problem_ids[history:]]
        return problems
