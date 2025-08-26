from apps.landing_page.views.home.home_view import HomeView
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse
from django.test import override_settings, TestCase, RequestFactory

from apps.landing_page.models.education import Education
from apps.landing_page.models.certification import Certification
from apps.landing_page.models.project import Project
from apps.landing_page.models.work_history import WorkHistory


@override_settings(SECRET_KEY="dummy-key")
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
            ),
            Certification.objects.create(
                name="cert",
                issuer="issuer",
                image="image",
                date="date",
                url="url",
                row=1,
            ),
            Project.objects.create(
                name="project",
                description="description",
                image="image",
                date="date",
                scroll_description=False,
                row=1,
                repositories=[{"name": "name", "url": "url"}],
            ),
            WorkHistory.objects.create(
                company_name="company_name",
                company_name_label="company_name_label",
                image="image",
                specialty="specialty",
                dates=["date123"],
                description="description",
            ),
        ]

        self.view.setup(self.request)
        self.assertEqual(response.status_code, 200)
