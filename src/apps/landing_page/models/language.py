from typing import Any

from django.db.models import CharField, IntegerField
from typing_extensions import override

from apps.landing_page.models.portfolio import Portfolio


class Language(Portfolio):
    name: CharField = CharField("Language", max_length=50)
    proficiency: CharField = CharField("Proficiency of the language", max_length=50)
    icon: CharField = CharField("Flag of the language", max_length=50)
    row: IntegerField = IntegerField("Row number of the language")

    @override
    def get_all(self) -> Any:
        return list(Language.objects.all().values())

    @override
    def transform(self) -> Any:
        languages_objs = self.get_all()

        self.clean(languages_objs)

        rows = {}
        result = []
        for language in languages_objs:
            row = language["row"]
            if row not in rows:
                rows[row] = {"row": row, "language": []}
                result.append(rows[row])
            language.pop("row")
            rows[row]["language"].append(language)

        return result

    @override
    def clean(self, languages_objs: list[Any]) -> None:
        for language in languages_objs:
            language.pop("id")
