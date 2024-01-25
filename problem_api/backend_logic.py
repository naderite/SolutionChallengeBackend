# backend_logic.py
from difflib import SequenceMatcher
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
        new = int(request.query_params.get("new"))
        return count, category, score, new

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
            fetched_problems = [problem for problem in problems]
            # shuffle problems to randomize deleted ones
            fetched_problems = random.sample(fetched_problems, len(fetched_problems))
            # Filter out problems that are too similar
            selected_problems = []
            selected_problems.append(fetched_problems[0])
            for fetched_problem in fetched_problems:
                should_add_problem = BackendLogic.filter_similar_problems(
                    fetched_problems, None, fetched_problem
                )
                if should_add_problem:
                    selected_problems.append(fetched_problem)
            all_problem_ids = [problem.id for problem in selected_problems]

            if len(selected_problems) > 5:
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
                remaining = count - selected_problems.count()
                selected_problems = BackendLogic.fetch_additional_problems(
                    selected_problems,
                    category,
                    score,
                    remaining,
                    1,
                    -1,
                )
        else:
            selected_problems = BackendLogic.fetch_additional_problems(
                selected_problems, category, score, count // 2, 1, +1
            )
            remaining = count - selected_problems.count()
            selected_problems = BackendLogic.fetch_additional_problems(
                selected_problems, category, score, remaining, 1, -1
            )
            if selected_problems.count() < count:
                remaining = count - selected_problems.count()

                selected_problems = BackendLogic.fetch_additional_problems(
                    selected_problems, category, score, remaining, 1, +1
                )
        return selected_problems

    @staticmethod
    def fetch_additional_problems(
        selected_problems, category, score, target_count, tolerance, direction
    ):
        additional_problems = []
        while len(additional_problems) < target_count and (
            100 >= (score + direction * tolerance) >= 0
        ):
            # Fetch additional problems

            fetched_problems = Question.objects.filter(
                category=category, difficulty_score=score + direction * tolerance
            )
            # shuffle problems to randomize deleted ones
            fetched_problems = fetched_problems.order_by("?")
            # Filter out problems that are too similar
            for fetched_problem in fetched_problems:
                should_add_problem = BackendLogic.filter_similar_problems(
                    selected_problems, additional_problems, fetched_problem
                )

                if should_add_problem:
                    additional_problems.append(fetched_problem)
            tolerance += 1
        additional_problems_ids = [problem.id for problem in additional_problems]
        selected_problems_ids = []
        if len(additional_problems_ids) > 0:
            selected_problems_ids = random.sample(
                additional_problems_ids, min(target_count, len(additional_problems_ids))
            )

        selected_problems = selected_problems.union(
            Question.objects.filter(id__in=selected_problems_ids)
        )
        return selected_problems

    @staticmethod
    def filter_similar_problems(
        existing_problems1, existing_problems2, fetched_problem
    ):
        for existing_problem in existing_problems1:
            if BackendLogic.are_problems_similar(
                existing_problem.problem, fetched_problem.problem
            ):
                return False
        if existing_problems2:
            for existing_problem in existing_problems2:
                if BackendLogic.are_problems_similar(
                    existing_problem.problem, fetched_problem.problem
                ):
                    return False

        return True

    @staticmethod
    def are_problems_similar(problem1, problem2):
        words1 = problem1.split()
        words2 = problem2.split()

        similarity_ratio = SequenceMatcher(None, words1, words2).ratio()

        return similarity_ratio >= 0.8

    @staticmethod
    def eval_student(category):
        id_10 = random.choice(EVAL_PROBLEMS_10[category])
        id_30 = random.choice(EVAL_PROBLEMS_30[category])
        id_40 = random.choice(EVAL_PROBLEMS_40[category])
        id_60 = random.choice(EVAL_PROBLEMS_60[category])
        id_70 = random.choice(EVAL_PROBLEMS_70[category])
        id_90 = random.choice(EVAL_PROBLEMS_90[category])

        problem_ids = [id_10, id_30, id_40, id_60, id_70, id_90]
        # Retrieve questions using the IDs
        problems = [Question.objects.get(id=id_) for id_ in problem_ids]
        return problems
