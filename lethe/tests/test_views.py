import json

from unittest.mock import patch

from lethe.exceptions import HermesBadResponseError
from lethe.tests.lethe_test_case import LetheTestCase


class TestViews(LetheTestCase):
    def test_healthz(self):
        resp = self.client.get("/healthz")
        self.assertEqual(resp.status_code, 204)

    def test_livez(self):
        resp = self.client.get("/livez")
        self.assertEqual(resp.status_code, 204)

    @patch("lethe.views.is_hermes_ready")
    def test_readyz_successful(self, mock_is_hermes_ready):
        mock_is_hermes_ready.return_value = (True, "")
        resp = self.client.get("/readyz")
        self.assertEqual(resp.status_code, 204)

    @patch("lethe.views.is_hermes_ready")
    def test_readyz_fail(self, mock_is_hermes_ready):
        mock_is_hermes_ready.return_value = (False, "nah mate hermes sad")
        resp = self.client.get("/readyz")
        error_json = json.loads(resp.data)
        self.assertIn("error", error_json)
        self.assertEqual(error_json["error"], "nah mate hermes sad")

    @patch("lethe.views.is_valid_token")
    def test_bad_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = False
        resp = self.client.get("/password/whatever")
        self.assertEqual(200, resp.status_code)
        self.assertIn(b"This link has expired", resp.data)

    @patch("lethe.views.is_valid_token")
    def test_good_token(self, mock_is_valid_token):
        mock_is_valid_token.return_value = True
        resp = self.client.get("/password/whatever")
        self.assertEqual(200, resp.status_code)
        self.assertIn(b"Confirm New Password", resp.data)

    @patch("lethe.views.is_valid_token")
    def test_hermes_error(self, mock_is_valid_token):
        mock_is_valid_token.side_effect = HermesBadResponseError()
        resp = self.client.get("/password/whatever")
        self.assertIn(b"Sorry, something has gone wrong on our end.", resp.data)

    def test_account_updated(self):
        resp = self.client.get("/password/account_updated")
        self.assertIn(b"Your account has been updated.", resp.data)

    def test_post_no_password(self):
        self.client.post("/password/whatever")
        self.assert_flash("You must provide your new password.")

    def test_post_no_password_confirmation(self):
        self.client.post("/password/whatever", data={"new_password": "whatever"})
        self.assert_flash("You must confirm your new password.")

    def test_post_non_matching_passwords(self):
        self.client.post("/password/whatever", data={"new_password": "foo", "confirm_new_password": "bar"})
        self.assert_flash("The passwords you entered did not match. Please try again.")

    @patch("lethe.views.requests.post")
    def test_update_account_good_pw(self, mock_post):
        mock_post.return_value.status_code = 200
        resp = self.client.post(
            "/password/whatever",
            data={"new_password": "Password123", "confirm_new_password": "Password123"},
            follow_redirects=True,
        )
        self.assertIn(b"Your account has been updated.", resp.data)

    @patch("lethe.views.requests.post")
    def test_update_account_bad_pw(self, mock_post):
        mock_post.return_value.status_code = 400
        resp = self.client.post(
            "/password/whatever",
            data={"new_password": "rubbishpassword", "confirm_new_password": "rubbishpassword"},
            follow_redirects=True,
        )
        self.assertIn(
            b"Password should be 8 or more characters, with at least 1 uppercase, 1 lowercase and a number", resp.data
        )

    @patch("lethe.views.requests.post")
    def test_update_account_broken(self, mock_post):
        mock_post.return_value.status_code = 404
        resp = self.client.post(
            "/password/whatever",
            data={"new_password": "rubbishpassword", "confirm_new_password": "rubbishpassword"},
            follow_redirects=True,
        )
        self.assertIn(b"This link has expired", resp.data)
