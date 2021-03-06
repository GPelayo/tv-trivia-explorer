import copy
import json
import os
from typing import List, Dict, Any

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from binge_companion.settings import VERSION
from superhero.models import Series, Trivia, Episode

LOCAL_TEST_JSON_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test-json')


class AuthenticationApiTestCase(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Test', password='Test-Password')

    def test_login(self):
        client = APIClient()
        is_logged_in = client.login(username='Test', password='Test-Password')
        self.assertTrue(is_logged_in)

    def test_get_auth_key(self):
        client = APIClient()
        auth_token_request = client.post('/api-token-auth/', data={'username': 'Test', 'password': 'Test-Password'})
        self.assertEqual(auth_token_request.status_code, 200, 'Auth token request endpoint failed to send auth token.')
        self.assertIn('token', auth_token_request.json())


class VersionTest(APITestCase):
    def test_version(self):
        client = APIClient()
        version_request = client.get('/version')
        self.assertEqual(version_request.status_code, 200, 'Version endpoint failed to send version number.')
        version_json = version_request.json()
        self.assertIn('version', version_json, 'Version field key in request is wrong.')
        self.assertEqual(version_json['version'], VERSION, 'Version endpoint doesn\'t properly send version send.')


class SeriesApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.maxDiff = None
        with open(os.path.join(LOCAL_TEST_JSON_DIRECTORY, 'setup-normal-series.json')) as setup_file:
            cls.setup_series_json = json.load(setup_file)
            series_json = copy.deepcopy(cls.setup_series_json)
            test_episode_json = series_json.pop('episodes')
            test_trivia_json = series_json.pop('series_wide_trivia')
            test_series = Series.objects.create(**series_json)
            for t in test_trivia_json:
                Trivia.objects.create(series=test_series, **t)
            for e in test_episode_json:
                episode_trivia_json = e.pop('trivia')
                test_episode = Episode.objects.create(series=test_series, **e)
                for t in episode_trivia_json:
                    Trivia.objects.create(series=test_series, episode=test_episode, **t)

    def setUp(self):
        User.objects.create_user(username='Test', password='Test-Password')
        auth_token_request = self.client.post('/api-token-auth/',
                                              data={'username': 'Test', 'password': 'Test-Password'})
        self.token = auth_token_request.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')

    def assertDictEqual(self, d1: Dict[str, Any], d2: Dict[str, Any],
                        msg: Any = ...) -> None:

        for k in set(list(d1.keys()) + list(d2.keys())):
            self.assertEqual(d1[k], d2[k], msg)

    def assertObjectList(self, l1: List[Any], l2: List[Any], primary_key_fieldname: str, msg: str = None):
        all_pks = set([l[primary_key_fieldname] for l in l1] + [l[primary_key_fieldname] for l in l2])
        for pk in all_pks:
            try:
                o1 = [l for l in l1 if l[primary_key_fieldname] == pk][0]
            except IndexError:
                assert False, f'No key {pk} in first list\n{l1}\n{l2}'
            try:
                o2 = [l for l in l1 if l[primary_key_fieldname] == pk][0]
            except IndexError:
                assert False, f'No key {pk} in first list'
            self.assertDictEqual(o1, o2)

    def assertValidResponseSeriesJson(self, response_series_json: Dict[str, Any], loaded_test_json: Dict[str, Any]):
        setup_episodes = loaded_test_json.pop('episodes')
        self.assertObjectList(setup_episodes, response_series_json.pop('episodes'), 'episode_id')
        episode_trivia = [t for e in setup_episodes for t in e['trivia']]
        setup_trivia = loaded_test_json.pop('series_wide_trivia', []) + episode_trivia
        self.assertObjectList(setup_trivia, response_series_json.pop('trivia', []), 'trivia_id')
        self.assertDictEqual(response_series_json, loaded_test_json)

    def test_getserieslist_normal(self):
        response = self.client.get(reverse('series-list'), follow=True)
        self.assertEqual(response.status_code, 200, response.data)
        test_json = response.json()
        setup_series = copy.deepcopy(self.setup_series_json)
        self.assertValidResponseSeriesJson(test_json[0], setup_series)

    def test_getseriesdetail_normal(self):
        response = self.client.get(reverse('series-detail', kwargs={'pk': 'BS'}), follow=True)
        self.assertEqual(response.status_code, 200, response.data)
        test_series_json = response.json()
        setup_series = copy.deepcopy(self.setup_series_json)
        self.assertValidResponseSeriesJson(test_series_json, setup_series)

    def test_deleteseries_nosetupseries(self):
        with open(os.path.join(LOCAL_TEST_JSON_DIRECTORY, 'edittest-editedseries-series.json'), 'r') as test_file:
            test_json = json.load(test_file)
            response = self.client.delete(reverse('series-detail', kwargs={'pk': 'BS'}), data=test_json, follow=True)
            self.assertEqual(response.status_code, 204, response.data)
            response = self.client.get(reverse('series-list'), follow=True)
            self.assertEqual(len(response.data), 0, response.data)
            response = self.client.get(reverse('series-detail', kwargs={'pk': 'BS'}), follow=True)
            self.assertEqual(response.status_code, 404, response.data)

    def test_createseries_normal(self):
        with open(os.path.join(LOCAL_TEST_JSON_DIRECTORY, 'createtest-normal-series.json'), 'r') as test_file:
            test_json = json.load(test_file)
            response = self.client.post(reverse('series-list'), data=test_json, format='json', follow=True)
            self.assertEqual(response.status_code, 201, response.data)

    def test_editseries_edittedseries(self):
        with open(os.path.join(LOCAL_TEST_JSON_DIRECTORY, 'edittest-editedseries-series.json'), 'r') as test_file:
            test_json = json.load(test_file)
            response = self.client.patch(reverse('series-detail', kwargs={'pk': 'BS'}), data=test_json, follow=True)
            self.assertEqual(response.status_code, 200, response.data)
            response = self.client.get(reverse('series-detail', kwargs={'pk': 'BS'}), follow=True)
            self.assertValidResponseSeriesJson(response.json(), test_json)
