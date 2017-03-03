from app.exceptions import HermesBadResponseError
from app.tests.lethe_test_case import LetheTestCase
from unittest.mock import patch


class TestViews(LetheTestCase):

    @patch('app.views.is_valid_token')
    def test_bad_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = False
        resp = self.client.get('/password/whatever')
        self.assertEqual(200, resp.status_code)
        self.assertIn(b'This link has expired', resp.data)

    @patch('app.views.is_valid_token')
    def test_good_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = True
        resp = self.client.get('/password/whatever')
        self.assertEqual(200, resp.status_code)
        self.assertIn(b'Confirm New Password', resp.data)

    @patch('app.views.is_valid_token')
    def test_hermes_error(self, mock_is_valid_token):
        mock_is_valid_token.side_effect = HermesBadResponseError()
        resp = self.client.get('/password/whatever')
        self.assertIn(b'Sorry, something has gone wrong on our end.', resp.data)

    def test_account_updated(self):
        resp = self.client.get('/password/account_updated')
        self.assertIn(b'Your account has been updated.', resp.data)

    def test_post_no_password(self):
        self.client.post('/password/whatever')
        self.assert_flash('You must provide your new password.')

    def test_post_no_password_confirmation(self):
        self.client.post('/password/whatever', data={'new_password': 'whatever'})
        self.assert_flash('You must confirm your new password.')

    def test_post_non_matching_passwords(self):
        self.client.post('/password/whatever', data={'new_password': 'foo', 'confirm_new_password': 'bar'})
        self.assert_flash('The passwords you entered did not match. Please try again.')

    @patch('app.views.requests.post')
    def test_update_account_good_pw(self, mock_post):
        mock_post.return_value.status_code = 200
        resp = self.client.post('/password/whatever', data={'new_password': 'Password123',
                                                            'confirm_new_password': 'Password123'},
                                follow_redirects=True)
        self.assertIn(b'Your account has been updated.', resp.data)

    @patch('app.views.requests.post')
    def test_update_account_bad_pw(self, mock_post):
        mock_post.return_value.status_code = 400
        resp = self.client.post('/password/whatever', data={'new_password': 'rubbishpassword',
                                                            'confirm_new_password': 'rubbishpassword'},
                                follow_redirects=True)
        self.assertIn(b'This password is invalid.', resp.data)

    @patch('app.views.requests.post')
    def test_update_account_broken(self, mock_post):
        mock_post.return_value.status_code = 404
        resp = self.client.post('/password/whatever', data={'new_password': 'rubbishpassword',
                                                            'confirm_new_password': 'rubbishpassword'},
                                follow_redirects=True)
        self.assertIn(b'Sorry, either your link has expired or something has gone wrong on our end.', resp.data)
