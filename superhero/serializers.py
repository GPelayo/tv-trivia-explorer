import logging

from superhero.models import Trivia, Episode, Series
from rest_framework import serializers

from superhero import helpers

log = logging.getLogger('django')


class TriviaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trivia
        fields = helpers.get_fields_from_model_name('Trivia')
        extra_kwargs = {
            'trivia_id': {'validators': []}
        }


class EpisodeSerializer(serializers.HyperlinkedModelSerializer):
    trivia = TriviaSerializer(many=True, required=False)

    class Meta:
        model = Episode
        fields = helpers.get_fields_from_model_name('Episode') + ['trivia']
        extra_kwargs = {
            'episode_id': {'validators': []}
        }

    def create(self, validated_data):
        trivia_data = validated_data.pop('trivia')
        episode = Episode.objects.create(**validated_data)
        log.info(f'Created Episode: {episode}')
        for trivia_json in trivia_data:
            new_trivia = Trivia.objects.create(episode=episode, **trivia_json)
            log.info(f'Created Trivia: {new_trivia}')
        return episode


class SeriesSerializer(serializers.HyperlinkedModelSerializer):
    episodes = EpisodeSerializer(many=True)
    series_wide_trivia = TriviaSerializer(many=True, required=False)

    class Meta:
        model = Series
        fields = helpers.get_fields_from_model_name('Series') + ['episodes', 'series_wide_trivia']
        extra_kwargs = {
            'series_id': {'validators': []}
        }

    def create(self, validated_data):
        episode_data = validated_data.pop('episodes')
        series_trivia_data = validated_data.pop('series_wide_trivia')
        series = Series.objects.create(**validated_data)
        log.info(f'Created Series: {series}')
        episode_trivia_ids = set()
        for episode in episode_data:
            self.create_linked_episode_data(episode, series, episode_trivia_ids=episode_trivia_ids)
        for trivia_json in series_trivia_data:
            if trivia_json['trivia_id'] not in episode_trivia_ids:
                new_trivia = Trivia.objects.create(series=series, **trivia_json)
                log.info(f'Created Trivia: {new_trivia}')
        return series

    @staticmethod
    def create_linked_episode_data(episode_data, series_instance, episode_trivia_ids):
        trivia_data = episode_data.pop('trivia')  if 'trivia' in episode_data else []
        episode = Episode.objects.create(series=series_instance, **episode_data)
        log.info(f'Created Episode: {episode}')
        for trivia_json in trivia_data:
            new_trivia = Trivia.objects.create(series=series_instance, episode=episode, **trivia_json)
            log.info(f'Created Trivia: {new_trivia}')
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
            new_trivia = Trivia.objects.create(series=series_instance, **kwargs, **trivia_json)
            log.info(f'Created Trivia: {new_trivia}')
        else:
            self.update_object(trv_instance, trivia_json, series=series_instance)
            log.info(f'Updated Trivia: {trv_instance}')

    def update(self, instance, validated_data):
        episode_data = validated_data.pop('episodes') if 'episodes' in validated_data else []
        series_trivia_data = validated_data.pop('trivia') if 'trivia' in validated_data else []
        self.update_object(instance, validated_data)
        log.info(f'Updated Series: {instance}')
        episode_trivia_ids = set()
        for episode_json in episode_data:
            trivia_data = episode_json.pop('trivia') if 'trivia' in validated_data else []
            try:
                ep_instance = Episode.objects.get(episode_id=episode_json['episode_id'])
            except Episode.DoesNotExist:
                self.create_linked_episode_data(episode_json, instance, series_trivia_data)
            else:
                self.update_object(ep_instance, episode_json, series=instance)
                log.info(f'Updated Episode: {ep_instance}')

            for trivia_json in trivia_data:
                self.update_trivia_object(instance, trivia_json['trivia_id'], trivia_json)
                episode_trivia_ids.add(trivia_json['trivia_id'])

        for trivia_json in series_trivia_data:
            if trivia_json['trivia_id'] in episode_trivia_ids:
                try:
                    trv_instance = Trivia.objects.get(trivia_id=trivia_json['trivia_id'])
                except Trivia.DoesNotExist:
                    new_trivia = Trivia.objects.create(series=instance, episode=ep_instance, **trivia_json)
                    log.info(f'Created Trivia: {new_trivia}')
                else:
                    self.update_object(trv_instance, trivia_json, series=instance)

        return instance
