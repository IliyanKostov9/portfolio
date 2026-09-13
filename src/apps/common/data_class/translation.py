from typing import Final, override

from portfolio.data_class.portfolio import Portfolio


class Translation(Portfolio):
    languages: Final[list[str]] = ["en", "bg", "fr", "ge"]

    @override
    @staticmethod
    def table_create(apps, app_name):
        translation_model = apps.get_model(app_name, "Translation")

        translation_model.objects.all().delete()

        for lang in Translation.languages:
            translation_model.objects.create(language=lang)
