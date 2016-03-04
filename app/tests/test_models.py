from app.exceptions import HermesBadResponseError
from app.models import is_valid_token
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
