from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from apps.resume.models.certification import Certification
from apps.resume.models.education import Education
from apps.resume.models.project import Project
from apps.resume.models.technology import Technology
from apps.resume.models.technology_category import TechnologyCategory
from apps.resume.models.work_history import WorkHistory
from apps.resume.views.home.home_view import HomeView


class HomeViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse("home"))
        self.view = HomeView()
        self.view.setup(self.request)
        settings.SECRET_KEY = "dummy-key"

    def test_get(self):
        response: WSGIRequest = self.client.get(
            "/",
        )

        self.request.technology_categories = [
            TechnologyCategory.objects.create(
                name="technologyCategory1",
            )
        ]

        self.request.technologies = [
            Technology.objects.create(
                name="technology1",
                icon="icon.svg",
                category=TechnologyCategory.objects.get(name="technologyCategory1"),
                row=1,
                page=1,
            )
        ]

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
        ]

        self.request.certifications = [
            Certification.objects.create(
                name="cert",
                issuer="issuer",
                image="image",
                date="date",
                url="url",
                row=1,
            ),
        ]

        self.request.projects = [
            Project.objects.create(
                name="project",
                description="description",
                image="image",
                date="date",
                scroll_description=False,
                row=1,
                repositories=[{"name": "name", "url": "url"}],
            ),
        ]

        self.request.work_histories = [
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
