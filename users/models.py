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

    total_gain = models.IntegerField(default=0)
    total_general = models.IntegerField(default=0)
    total_probability = models.IntegerField(default=0)
    total_geometry = models.IntegerField(default=0)
    total_physics = models.IntegerField(default=0)
    total_other = models.IntegerField(default=0)

    def __str__(self):
        return self.uid
