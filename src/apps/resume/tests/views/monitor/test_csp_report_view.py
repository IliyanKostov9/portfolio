from django.test import TestCase
from django.core.handlers.wsgi import WSGIRequest


class CSPReportTestCase(TestCase):
    def test_post(self):
        response: WSGIRequest = self.client.post(
            "/monitor/csp-report",
            content_type="application/json",
            HTTP_USER_AGENT="Firefox/1.0",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), "Report send!")

        response_fault: WSGIRequest = self.client.post(
            "/monitor/csp-report",
            content_type="text/html",
            HTTP_USER_AGENT="Firefox/1.0",
        )
        self.assertEqual(response_fault.status_code, 400)
        self.assertEqual(response_fault.content.decode("utf-8"), "Invalid content type")
