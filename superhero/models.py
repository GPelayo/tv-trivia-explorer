from django.db import models
from django.core.validators import MinValueValidator


class Series(models.Model):
    series_id = models.TextField(primary_key=True)
    name = models.TextField()
    season_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    thumbnail_url = models.URLField()


class Episode(models.Model):
    episode_id = models.TextField(primary_key=True)
    name = models.TextField()
    season = models.TextField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)


class Trivia(models.Model):
    trivia_id = models.TextField(primary_key=True)
    score = models.PositiveIntegerField()
    score_denominator = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    text = models.TextField()
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)


class TriviaTag(models.Model):
    text = models.TextField()
    parent = models.ForeignKey(Trivia, on_delete=models.CASCADE)
