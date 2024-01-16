from django.db import models


class UserScores(models.Model):
    uid = models.CharField(max_length=100, unique=True)

    # Scores for different categories
    gain = models.IntegerField(default=0)
    general = models.IntegerField(default=0)
    probability = models.IntegerField(default=0)
    geometry = models.IntegerField(default=0)
    physics = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
