from flask_testing import TestCase

from lethe.wsgi import create_app


class Testing:
    TESTING = True
    LETHE_DEBUG = True
    SECRET_KEY = "\xb9\xd1\xc13\xf3\x04\xdf\x89\xbd\xca\x8e\x16\xda\xcaj\x04\x88\xd1\x13;\xcc\xb8\x927"


class LetheTestCase(TestCase):
    def create_app(self):
        return create_app(Testing)

    def assert_flash(self, expected_message):
        with self.client.session_transaction() as session:
            try:
                category, message = session["_flashes"][0]
            except KeyError:
                raise AssertionError("Nothing was flashed.")
            self.assertEqual(expected_message, message)

    def assert_in_flash(self, expected_message):
        with self.client.session_transaction() as session:
            try:
                category, message = session["_flashes"][0]
            except KeyError:
                raise AssertionError("Nothing was flashed.")
            self.assertIn(expected_message, message)
