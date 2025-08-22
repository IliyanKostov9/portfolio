from typing import Any

from apps.landing_page.data_class.portfolio.education import (
    Education as EducationDataClass,
)
from apps.landing_page.models.education import Education
from apps.landing_page.tests.models.portfolio import Portfolio


class EducationTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        education_model: Any = self.model.apps.get_model("landing_page", "Education")

        educations_dc: list[Any] = EducationDataClass.from_yaml(
            "portfolio/education.yaml"
        )

        for education_dc in educations_dc:
            education: Education = education_model.objects.get(
                specialty=education_dc.specialty, degree=education_dc.degree
            )

            self.assertEqual(education_dc.university_name, education.university_name)
            self.assertEqual(education_dc.description, education.description)
            self.assertEqual(
                education_dc.scroll_description, education.scroll_description
            )
            self.assertEqual(education_dc.image, education.image)
            self.assertEqual(education_dc.href_tooltip, education.href_tooltip)
            self.assertEqual(education_dc.href_title, education.href_title)
            self.assertEqual(education_dc.date, education.date)
            self.assertEqual(education_dc.gpa, education.gpa)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        educations: list[Education] = (
            self.model.apps.get_model("landing_page", "Education")
            .objects.all()
            .values()
        )

        education_model = Education()
        education_model.clean(educations)

        for education in educations:
            self.assertIsNone(education.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        education_model: Any = self.model.apps.get_model("landing_page", "Education")

        education = Education()
        educations = education.transform()

        educations_db = education_model.objects.all().values()
        education.clean(educations_db)

        self.assertListEqual(educations, list(educations_db))

        super().tearDownClass()
