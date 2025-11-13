from apps.resume.data_class.certification import Certification
from apps.resume.data_class.education import Education
from apps.resume.data_class.language_proficiency import LanguageProficiency
from apps.resume.data_class.project import Project
from apps.resume.data_class.technology import Technology
from apps.resume.data_class.technology_category import TechnologyCategory
from apps.resume.data_class.translation import Translation
from apps.resume.data_class.work_history import WorkHistory


def init(apps, schema_editor):
    Translation.table_create(apps)
    TechnologyCategory.table_create(apps)
    Technology.table_create(apps)

    WorkHistory.table_create(apps)
    Education.table_create(apps)
    Certification.table_create(apps)
    Project.table_create(apps)
    LanguageProficiency.table_create(apps)


def init_reverse(apps, schema_editor):
    """
    NOTE: Keep it because it'll complain when you make `make sql-init-test`
    """
