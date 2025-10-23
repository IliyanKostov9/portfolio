from apps.resume.views.blogs.blogs_view import BlogsView
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.test import TestCase, RequestFactory

from django.conf import settings


class BlogsTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("blogs"))
        self.view = BlogsView()
        self.view.setup(self.request)
        settings.SECRET_KEY = "dummy-key"

    def test_get(self):
        response: WSGIRequest = self.client.get(
            "/",
        )

        self.view.setup(self.request)
        self.assertEqual(response.status_code, 200)
