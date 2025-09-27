from apps.resume.models.technology_category import TechnologyCategory
from apps.resume.tests.models.portfolio import Portfolio


class TechonolgyCategoryTestCase(Portfolio):
    def test_data_types(self):
        self.setUp()

        technology_category: TechnologyCategory = self.model.apps.get_model(
            "resume", "TechnologyCategory"
        ).objects.get(name="Programming languages")

        self.assertEqual(isinstance(technology_category.name, str), True)
        super().tearDownClass()
