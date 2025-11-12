from typing import Any

from apps.resume.data_class.education import Education as EducationDataClass
from apps.resume.models.education import Education
from apps.resume.tests.models.portfolio import Portfolio


class EducationTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        education_model: Any = self.model.apps.get_model("resume", "Education")

        educations_dc: list[Any] = EducationDataClass.from_yaml("education.yaml")

        for education_dc in educations_dc:
            for lang in self.languages:
                education: Education = education_model.objects.get(
                    specialty=getattr(education_dc, lang + "_specialty"),
                    degree=getattr(education_dc, lang + "_degree"),
                )

                self.assertEqual(
                    getattr(education_dc, lang + "_university_name"),
                    education.university_name,
                )
                self.assertEqual(
                    getattr(education_dc, lang + "_description"), education.description
                )
                self.assertEqual(
                    education_dc.scroll_description, education.scroll_description
                )
                self.assertEqual(education_dc.image, education.image)
                self.assertEqual(education_dc.href_tooltip, education.href_tooltip)
                self.assertEqual(
                    getattr(education_dc, lang + "_href_title"), education.href_title
                )
                self.assertEqual(education_dc.date, education.date)
                self.assertEqual(education_dc.gpa, education.gpa)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        educations: list[Education] = (
            self.model.apps.get_model("resume", "Education").objects.all().values()
        )

        education_model = Education()
        education_model.clean(educations)

        for education in educations:
            self.assertIsNone(education.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        education_model: Any = self.model.apps.get_model("resume", "Education")

        education = Education()
        educations = education.transform()

        educations_db = education_model.objects.get(language_id="en")
        education.clean(educations_db)

        self.assertListEqual(educations, list(educations_db))

        super().tearDownClass()
