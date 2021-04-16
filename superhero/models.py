from django.db import models
from django.core.validators import MinValueValidator


class Series(models.Model):
    name = models.TextField()
    season_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    thumbnail_url = models.URLField()


class Episode(models.Model):
    name = models.TextField()
    season = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)


class Trivia(models.Model):
    score = models.PositiveIntegerField()
    score_denominator = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    text = models.TextField()
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)


class TriviaTag(models.Model):
    text = models.TextField()
    parent = models.ForeignKey(Trivia, on_delete=models.CASCADE)
