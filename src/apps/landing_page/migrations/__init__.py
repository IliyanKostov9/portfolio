from apps.landing_page.data_class.portfolio.certification import Certification
from apps.landing_page.data_class.portfolio.education import Education
from apps.landing_page.data_class.portfolio.project import Project
from apps.landing_page.data_class.portfolio.technology import Technology
from apps.landing_page.data_class.portfolio.technology_category import (
    TechnologyCategory,
)
from apps.landing_page.data_class.portfolio.work_history import WorkHistory


def init(apps, schema_editor):
    TechnologyCategory.table_create(apps)
    Technology.table_create(apps)

    WorkHistory.table_create(apps)
    Education.table_create(apps)
    Certification.table_create(apps)
    Project.table_create(apps)


def init_reverse(apps, schema_editor):
    """
    NOTE: Keep it because it'll complain when you make `make sql-init-test`
    """
