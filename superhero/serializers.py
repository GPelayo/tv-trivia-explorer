from superhero.models import Trivia, Episode, Series
from rest_framework import serializers

from superhero import helpers


class TriviaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trivia
        fields = helpers.get_fields_from_model_name('Trivia')
        extra_kwargs = {
            'trivia_id': {'validators': []}
        }


class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    trivia_set = TriviaSerializer(many=True)

    class Meta:
        model = Episode
        fields = helpers.get_fields_from_model_name('Episode') + ['trivia_set']
        extra_kwargs = {
            'episode_id': {'validators': []}
        }

    def create(self, validated_data):
        trivia_data = validated_data.pop('trivia_set')
        episode = Episode.objects.create(**validated_data)
        for trivia_json in trivia_data:
            Trivia.objects.create(episode=episode, **trivia_json)
        return episode


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    episode_set = EpisodeSerializer(many=True)
    trivia_set = TriviaSerializer(many=True)

    class Meta:
        model = Series
        fields = helpers.get_fields_from_model_name('Series') + ['episode_set', 'trivia_set']
        extra_kwargs = {
            'series_id': {'validators': []}
        }

    def create(self, validated_data):
        episode_data = validated_data.pop('episode_set')
        series_trivia_data = validated_data.pop('trivia_set')
        series = Series.objects.create(**validated_data)
        episode_trivia_ids = set()
        for episode_json in episode_data:
            self.create_linked_episode_data(episode_data, series, episode_trivia_ids=episode_trivia_ids)
        for trivia_json in series_trivia_data:
            if trivia_json['trivia_id'] in episode_trivia_ids:
                Trivia.objects.create(series=series, **trivia_json)
        return series

    @staticmethod
    def create_linked_episode_data(episode_data, series_instance, episode_trivia_ids):
        trivia_data = episode_data.pop('trivia_set')
        episode = Episode.objects.create(series=series_instance, **episode_data)
        for trivia_json in trivia_data:
            Trivia.objects.create(series=series_instance, episode=episode, **trivia_json)
            episode_trivia_ids.add(trivia_json['trivia_id'])

    @staticmethod
    def update_object(instance, new_data, **kwargs):
        new_data = dict(new_data)
        new_data.update(kwargs)
        for field in instance._meta.fields:
            if field.name in new_data:
                setattr(instance, field.name, new_data[field.name])
        instance.save()

    def update_trivia_object(self, series_instance, trivia_id, trivia_json, **kwargs):
        try:
            trv_instance = Trivia.objects.get(trivia_id=trivia_id)
        except Trivia.DoesNotExist:
            Trivia.objects.create(series=series_instance, **kwargs, **trivia_json)
        else:
            self.update_object(trv_instance, trivia_json, series=series_instance)

    def update(self, instance, validated_data):
        episode_data = validated_data.pop('episode_set')
        series_trivia_data = validated_data.pop('trivia_set')
        self.update_object(instance, validated_data)
        episode_trivia_ids = set()
        for episode_json in episode_data:
            trivia_data = episode_json.pop('trivia_set')
            try:
                ep_instance = Episode.objects.get(episode_id=episode_json['episode_id'])
            except Episode.DoesNotExist:
                self.create_linked_episode_data(episode_json, instance, series_trivia_data)
            else:
                self.update_object(ep_instance, episode_json, series=instance)

            for trivia_json in trivia_data:
                self.update_trivia_object(instance, trivia_json['trivia_id'], trivia_json)
                episode_trivia_ids.add(trivia_json['trivia_id'])

        for trivia_json in series_trivia_data:
            if trivia_json['trivia_id'] in episode_trivia_ids:
                try:
                    trv_instance = Trivia.objects.get(trivia_id=trivia_json['trivia_id'])
                except Trivia.DoesNotExist:
                    Trivia.objects.create(series=instance, episode=ep_instance, **trivia_json)
                else:
                    self.update_object(trv_instance, trivia_json, series=instance)

        return instance
