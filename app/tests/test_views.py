from app.tests.lethe_test_case import LetheTestCase


class TestViews(LetheTestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(b'Hello from Lethe!', resp.data)
