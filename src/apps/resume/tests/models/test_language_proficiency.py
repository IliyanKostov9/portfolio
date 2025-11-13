from typing import Any

from apps.resume.data_class.language_proficiency import (
    LanguageProficiency as LanguageProficiencyDataClass,
)
from apps.resume.models.language_proficiency import LanguageProficiency
from apps.resume.tests.models.portfolio import Portfolio


class LanguageProficiencyTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        language_model: Any = self.model.apps.get_model("resume", "LanguageProficiency")

        languages_dc: list[Any] = LanguageProficiencyDataClass.from_yaml(
            "language_proficiency.yaml"
        )

        for language_dc in languages_dc:
            for lang in self.languages:
                language: LanguageProficiency = language_model.objects.get(
                    name=getattr(language_dc, lang + "_name")
                )

                self.assertEqual(getattr(language_dc, lang + "_name"), language.name)
                self.assertEqual(language_dc.icon, language.icon)
                self.assertEqual(language_dc.proficiency, language.proficiency)
                self.assertEqual(language_dc.row, language.row)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        languages: list[LanguageProficiency] = (
            self.model.apps.get_model("resume", "LanguageProficiency")
            .objects.all()
            .values()
        )

        language_model = LanguageProficiency()
        language_model.clean(languages)

        for language in languages:
            self.assertIsNone(language.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        language_model: Any = self.model.apps.get_model("resume", "LanguageProficiency")

        language = LanguageProficiency()
        language_transformed = language.transform()

        for langs in language_transformed:
            self.assertTrue(langs.get("row"))
            self.assertTrue(langs.get("language"))

            for lang in langs["language"]:
                lang_model = language_model.objects.get(name=lang["name"])

                self.assertEqual(lang_model.proficiency, lang["proficiency"])
                self.assertEqual(lang_model.icon, lang["icon"])

                self.assertIsNotNone(lang["level"])
                self.assertIsNotNone(lang["level_color"])

        super().tearDownClass()
