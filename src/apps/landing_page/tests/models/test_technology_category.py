from apps.landing_page.models.technology_category import TechnologyCategory
from apps.landing_page.tests.models.portfolio import Portfolio


class TechonolgyCategoryTestCase(Portfolio):
    def test_data_types(self):
        self.setUp()

        technology_category: TechnologyCategory = self.model.apps.get_model(
            "landing_page", "TechnologyCategory"
        ).objects.get(name="Programming languages")

        self.assertEqual(isinstance(technology_category.name, str), True)
        super().tearDownClass()
