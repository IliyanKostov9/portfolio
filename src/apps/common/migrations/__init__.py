from apps.common.data_class.translation import Translation


def init(apps, schema_editor):
    Translation.table_create(apps, "common")


def init_reverse(apps, schema_editor):
    """
    NOTE: Keep it because it'll complain when you make `make sql-init-test`
    """
