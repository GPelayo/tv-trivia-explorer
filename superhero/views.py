from django.shortcuts import render
from rest_framework import viewsets
from superhero.models import Series, Episode, Trivia
from superhero.serializers import SeriesSerializer, EpisodeSerializer, TriviaSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class EpisodeViewSet(viewsets.ModelViewSet):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer


class TriviaViewSet(viewsets.ModelViewSet):
    queryset = Trivia.objects.all()
    serializer_class = TriviaSerializer
