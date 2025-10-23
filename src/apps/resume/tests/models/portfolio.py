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
                ("resume", "0002_auto_20251022_2256")
            )
