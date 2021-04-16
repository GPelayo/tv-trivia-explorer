from superhero.models import Trivia, Episode, Series
from rest_framework import serializers

from superhero import helpers


class TriviaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trivia
        fields = helpers.get_fields_from_model_name('Trivia')


class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    trivia_set = TriviaSerializer(many=True)

    class Meta:
        model = Episode
        fields = helpers.get_fields_from_model_name('Episode') + ['trivia_set']

    def create(self, validated_data):
        trivia_data = validated_data.pop('trivia_set')
        episode = Episode.objects.create(**validated_data)
        for trivia_json in trivia_data:
            Trivia.objects.create(episode=episode, **trivia_json)
        return episode


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    episode_set = EpisodeSerializer(many=True)

    class Meta:
        model = Series
        fields = helpers.get_fields_from_model_name('Series') + ['episode_set']

    def create(self, validated_data):
        episode_data = validated_data.pop('episode_set')
        series = Series.objects.create(**validated_data)
        for episode_json in episode_data:
            trivia_data = episode_json.pop('trivia_set')
            episode = Episode.objects.create(series=series, **episode_json)
            for trivia_json in trivia_data:
                Trivia.objects.create(episode=episode, **trivia_json)
        return series
