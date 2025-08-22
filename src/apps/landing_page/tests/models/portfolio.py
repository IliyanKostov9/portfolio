from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TransactionTestCase
from django_test_migrations.migrator import Migrator


class Portfolio(TransactionTestCase):
    model: ProjectState

    def setUp(self):
        with connection.constraint_checks_disabled():
            migrator = Migrator(database="default")
            self.model = migrator.apply_initial_migration(
                ("landing_page", "0002_auto_20250822_1716")
            )
