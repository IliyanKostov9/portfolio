from typing import Any

from apps.resume.data_class.technology_category import (
    TechnologyCategory as TechnologyCategoryDataClass,
)
from apps.resume.models.technology_category import TechnologyCategory
from apps.resume.tests.models.portfolio import Portfolio


class TechonolgyCategoryTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        technology_category_model: Any = self.model.apps.get_model(
            "resume", "TechnologyCategory"
        )

        technology_technologies_dc: list[Any] = TechnologyCategoryDataClass.from_yaml(
            "technology_category.yaml"
        )

        for technology_category_dc in technology_technologies_dc:
            technology_category: TechnologyCategory = (
                technology_category_model.objects.get(name=technology_category_dc.name)
            )

            self.assertEqual(technology_category_dc.name, technology_category.name)

        super().tearDownClass()
