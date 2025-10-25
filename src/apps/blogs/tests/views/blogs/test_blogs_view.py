from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.blogs.models.blog import Blog
from apps.blogs.models.blog_category import BlogCategory
from apps.blogs.views.blogs.blogs_view import BlogsView


class BlogsTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("blogs"))
        self.view = BlogsView()
        self.view.setup(self.request)
        settings.SECRET_KEY = "dummy-key"

    def test_get(self):
        response: WSGIRequest = self.client.get(
            "/blogs/",
        )

        self.request.blogs = [
            BlogCategory.objects.create(name="blogCategory1"),
        ]
        blog_category1 = BlogCategory.objects.get(name="blogCategory1")

        self.request.blogs = [
            Blog.objects.create(
                title="Blog1",
                description="Description of a blog",
                image_preview="image.png",
                date="2025-01-01",
                url="the-start-of-something-new",
                read_time_mins=3,
                row=1,
                category=blog_category1,
            ),
        ]

        self.view.setup(self.request)
        self.assertEqual(response.status_code, 200)
