from typing import Any

from apps.landing_page.data_class.portfolio.technology import (
    Technology as TechnologyDataClass,
)
from apps.landing_page.models.technology import Technology
from apps.landing_page.tests.models.portfolio import Portfolio


class TechonolgyTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        technology_model: Any = self.model.apps.get_model("landing_page", "Technology")

        technologies_dc: list[Any] = TechnologyDataClass.from_yaml(
            "portfolio/technology.yaml"
        )

        for technology_dc in technologies_dc:
            technology: Technology = technology_model.objects.get(
                name=technology_dc.name
            )

            self.assertEqual(technology_dc.name, technology.name)
            self.assertEqual(technology_dc.icon, technology.icon)
            self.assertEqual(technology_dc.category, technology.category.name)
            self.assertEqual(technology_dc.page, technology.page)
            self.assertEqual(technology_dc.row, technology.row)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        technologies: list[Technology] = (
            self.model.apps.get_model("landing_page", "Technology")
            .objects.all()
            .values()
        )

        technology_model = Technology()
        technology_model.clean(technologies)

        for technology in technologies:
            self.assertIsNone(technology.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        technology_category_model: Any = self.model.apps.get_model(
            "landing_page", "TechnologyCategory"
        )

        technology = Technology()
        technologies = technology.transform()
        self.assertTrue(technologies.get("pages"), True)

        for _, page_value in technologies.items():
            for page_name, category_value in page_value.items():
                valid_pages = [1, 2]
                self.assertTrue(int(page_name) in valid_pages, True)
                self.assertTrue(category_value.get("categories"), True)

                for _, languages in category_value.items():
                    for name, language in languages.items():
                        self.assertIsNotNone(
                            technology_category_model.objects.get(name=name)
                        )

                        for rows_name, _ in language.items():
                            self.assertTrue(rows_name, "rows")

        super().tearDownClass()
