from typing import Any, Final

from django.db.models import CASCADE, CharField, ForeignKey, IntegerField
from django.forms.models import model_to_dict
from django.utils.translation import get_language
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.translation import Translation
from portfolio.monitor.log import logger

LANGUAGE_LEVEL_PROFICIENCY: Final[dict[str, int]] = {
    "Beginner": 25,
    "Intermediate": 50,
    "Advanced": 75,
    "Fluent": 100,
    "Native": 100,
}

PROFICIENCY_TRANSLATIONS = {
    "en": {
        "Beginner": "Beginner",
        "Intermediate": "Intermidiate",
        "Advanced": "Advanced",
        "Fluent": "Fluent",
        "Native": "Native",
    },
    "bg": {
        "Beginner": "Начинаещ",
        "Intermediate": "Междинно ниво",
        "Advanced": "Силен",
        "Fluent": "Владее свободно",
        "Native": "Местен",
    },
    "fr": {
        "Beginner": "Débutant",
        "Intermediate": "Intermédiaire",
        "Advanced": "Avancé",
        "Fluent": "Courant",
        "Native": "Indigène",
    },
    "ge": {
        "Beginner": "Anfänger",
        "Intermediate": "Dazwischenliegend",
        "Advanced": "Fortschrittlich",
        "Fluent": "Fließend",
        "Native": "Einheimisch",
    },
}

LANGUAGE_LEVEL_COLORS: Final[dict[str, str]] = {
    "Beginner": "bg-danger",
    "Intermediate": "bg-warning",
    "Advanced": "",
    "Fluent": "bg-success",
    "Native": "bg-success",
}


class LanguageProficiency(Portfolio):
    name: CharField = CharField("Name of the language", max_length=50)
    proficiency: CharField = CharField("Proficiency of the language", max_length=50)
    icon: CharField = CharField("Flag of the language", max_length=50)
    row: IntegerField = IntegerField("Row number of the language")
    language: ForeignKey = ForeignKey(
        Translation,
        verbose_name="Translated language name",
        on_delete=CASCADE,
    )
    LOG = logger.bind(module="language_model")

    @override
    def get_all(self) -> Any:
        return list(LanguageProficiency.objects.filter(language=get_language()))

    @override
    def transform(self) -> Any:
        languages_objs = [model_to_dict(wh) for wh in self.get_all()]

        self.clean(languages_objs)

        rows = {}
        result = []
        try:
            for language in languages_objs:
                row = language["row"]
                if row not in rows:
                    rows[row] = {"row": row, "language": []}
                    result.append(rows[row])
                language.pop("row")

                language["level"] = LANGUAGE_LEVEL_PROFICIENCY.get(
                    language["proficiency"]
                )
                language["level_color"] = LANGUAGE_LEVEL_COLORS.get(
                    language["proficiency"]
                )
                rows[row]["language"].append(language)

                proficiency: str = language["proficiency"]
                language["proficiency"] = PROFICIENCY_TRANSLATIONS[get_language()][
                    proficiency
                ]
                print(f"Proficiency: {proficiency}")

        except KeyError:
            logger.error(
                "Keyerror when trying to retrieve the translated text for language!"
            )

        return result

    @override
    def clean(self, languages_objs: list[Any]) -> None:
        for language in languages_objs:
            language.pop("id")
