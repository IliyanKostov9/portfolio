from typing import Final

from django.db import connection
from django.db.migrations.state import ProjectState
from django.test import TransactionTestCase
from django_test_migrations.migrator import Migrator


class Portfolio(TransactionTestCase):
    model: ProjectState

    languages: Final[list[str]] = ["en", "bg", "fr", "ge"]

    def setUp(self):
        with connection.constraint_checks_disabled():
            migrator = Migrator(database="default")
            self.model = migrator.apply_initial_migration(
                ("resume", "0002_resume_migrate")
            )
