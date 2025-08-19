from django.test import TestCase

from apps.landing_page.models.technology_category import TechnologyCategory


class TechonolgyCategoryTestCase(TestCase):
    def test_data_types(self):
        technology_category: TechnologyCategory = TechnologyCategory.objects.get(
            name="Programming languages"
        )

        self.assertEqual(isinstance(technology_category.name), str)
