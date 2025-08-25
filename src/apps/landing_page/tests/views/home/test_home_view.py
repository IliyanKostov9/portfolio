from django.test import RequestFactory, TestCase

from apps.landing_page.views.home.home_view import HomeView
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse

from apps.landing_page.models.education import Education


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("home"))
        self.view = HomeView()
        self.view.setup(self.request)

    def test_get(self):
        response: WSGIRequest = self.client.get(
            "/",
        )

        self.request.educations = [
            Education.objects.create(
                degree="degree",
                specialty="specialty",
                university_name="university_name",
                description="description",
                scroll_description=True,
                image="image",
                href_tooltip="href_tooltip",
                href_title="href_title",
                date="date",
                gpa="gpa",
            )
        ]

        self.view.setup(self.request)
        self.assertEqual(response.status_code, 200)
