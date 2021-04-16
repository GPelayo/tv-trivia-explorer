from superhero import models
from rest_framework import serializers

from superhero import helpers


class TriviaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Trivia
        fields = helpers.get_fields_from_model_name('Trivia')


class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    trivia = TriviaSerializer(many=True)

    class Meta:
        model = models.Episode
        fields = helpers.get_fields_from_model_name('Episode') + ['trivia']


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    episodes = EpisodeSerializer(many=True)

    class Meta:
        model = models.Series
        fields = helpers.get_fields_from_model_name('Series') + ['episodes']
