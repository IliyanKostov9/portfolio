from django.test import TestCase
from django.core.handlers.wsgi import WSGIRequest


class VoiceTestCase(TestCase):
    def test_post(self):
        response: WSGIRequest = self.client.post(
            "/home/voice/",
            data={
                "text": "This is a test",
            },
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 200)

        response: WSGIRequest = self.client.post(
            "/home/voice/",
            data={"no_text": "This should fail"},
            content_type="application/json",
            follow=False,
        )

        self.assertEqual(response.status_code, 400)
