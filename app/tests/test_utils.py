import unittest

from app.utils import url_for


class TestUtils(unittest.TestCase):
    def test_url_for(self):
        url = url_for('/test_url', 'test_arg1', 'test_arg2')
        self.assertTrue(url.endswith('/test_url/test_arg1/test_arg2'))
