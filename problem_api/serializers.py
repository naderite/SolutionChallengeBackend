# serializers.py
from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "problem",
            "rationale",
            "options",
            "correct",
            "category",
            "difficulty_score",
        ]
