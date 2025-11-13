from dataclasses import dataclass

from typing_extensions import override

from apps.resume.data_class.portfolio import Portfolio


@dataclass(frozen=True)
class Translation(Portfolio):
    @override
    @staticmethod
    def table_create(apps):
        translation_model = apps.get_model(Portfolio.app_name, "Translation")

        translation_model.objects.all().delete()

        for lang in Portfolio.languages:
            translation_model.objects.create(language=lang)
