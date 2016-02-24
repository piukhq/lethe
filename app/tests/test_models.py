from app.models import is_valid_token
from app.tests.lethe_test_case import LetheTestCase


class TestModels(LetheTestCase):
    def test_invalid_token(self):
        self.assertFalse(is_valid_token('bad bad bad'))

    def test_valid_token(self):
        self.assertTrue(is_valid_token('valid_token'))
