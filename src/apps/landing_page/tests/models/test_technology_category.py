from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TransactionTestCase
from django_test_migrations.migrator import Migrator

from apps.landing_page.models.technology_category import TechnologyCategory


class TechonolgyCategoryTestCase(TransactionTestCase):
    model: ProjectState

    def setUp(self):
        with connection.constraint_checks_disabled():
            migrator = Migrator(database="default")
            self.model = migrator.apply_initial_migration(
                ("landing_page", "0002_auto_20250820_2315")
            )

    def test_data_types(self):
        self.setUp()

        technology_category: TechnologyCategory = self.model.apps.get_model(
            "landing_page", "TechnologyCategory"
        ).objects.get(name="Programming languages")

        self.assertEqual(isinstance(technology_category.name, str), True)
        super().tearDownClass()
