from typing import Final


POSTGRES_TABLES: Final[list[str]] = ["user", "comment"]


class PortfolioRouter:
    postgres_database: str = "portfolio"
    default_database: str = "default"

    def db_for_read(self, model, **hints):
        if model._meta.model_name in POSTGRES_TABLES:
            return self.postgres_database
        else:
            return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in POSTGRES_TABLES:
            return self.postgres_database
        else:
            return None

    def allow_migrate(self, database, app_label, model=None, **hints):
        if database in POSTGRES_TABLES:
            return database == "portfolio"
        else:
            return database == "default"
