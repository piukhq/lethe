import requests.exceptions
from app.exceptions import HermesBadResponseError
from app.models import is_valid_token, is_hermes_ready
from app.tests.lethe_test_case import LetheTestCase
from unittest.mock import patch


class TestModels(LetheTestCase):

    @patch('app.models.requests.post')
    def test_invalid_token(self, mock_post):
        mock_post.return_value.status_code = 404
        self.assertFalse(is_valid_token('bad bad bad'))

    @patch('app.models.requests.post')
    def test_valid_token(self, mock_post):
        mock_post.return_value.status_code = 200
        self.assertTrue(is_valid_token('maybe a valid token'))

    @patch('app.models.requests.post')
    def test_hermes_error(self, mock_post):
        mock_post.return_value.status_code = 500
        with self.assertRaises(HermesBadResponseError) as context:
            is_valid_token('')
        self.assertIn('Hermes returned error code 500', context.exception.args)

        mock_post.reset_mock()
        mock_post.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(HermesBadResponseError) as context:
            is_valid_token('')
        self.assertIn('Failed to connect to Hermes. Error: ', context.exception.args)

    @patch('app.models.requests.get')
    def test_hermes_ready(self, mock_get):
        mock_get.return_value.status_code = 200
        ok, _ = is_hermes_ready()
        self.assertTrue(ok)

    @patch('app.models.requests.get')
    def test_hermes_notready(self, mock_get):
        mock_get.return_value.status_code = 500
        ok, err = is_hermes_ready()
        self.assertFalse(ok)
        self.assertIn('500', err)

    @patch('app.models.requests.get')
    def test_hermes_connectionerr(self, mock_get):
        mock_get.side_effect = ConnectionError
        ok, err = is_hermes_ready()
        self.assertFalse(ok)
        self.assertIn('error:', err)
