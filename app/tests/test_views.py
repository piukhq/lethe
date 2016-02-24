from unittest.mock import patch

from app.tests.lethe_test_case import LetheTestCase


class TestViews(LetheTestCase):
    def test_no_token(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)
        self.assertIn(b'This link has expired', resp.data)

    @patch('app.views.is_valid_token')
    def test_bad_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = False
        resp = self.client.get('/whatever')
        self.assertEqual(200, resp.status_code)
        self.assertIn(b'This link has expired', resp.data)

    @patch('app.views.is_valid_token')
    def test_good_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = True
        resp = self.client.get('/whatever')
        self.assertEqual(200, resp.status_code)
        self.assertIn(b'Confirm New Password', resp.data)
