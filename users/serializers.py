from rest_framework import serializers
from .models import UserScores


class UserScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScores
        fields = "__all__"
