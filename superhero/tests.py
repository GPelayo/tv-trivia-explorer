from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase

from binge_companion.settings import VERSION


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
