from typing import Any

from apps.resume.data_class.language import Language as LanguageDataClass
from apps.resume.models.language import Language
from apps.resume.tests.models.portfolio import Portfolio


class LanguageTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        language_model: Any = self.model.apps.get_model("resume", "Language")

        languages_dc: list[Any] = LanguageDataClass.from_yaml("language.yaml")

        for language_dc in languages_dc:
            language: Language = language_model.objects.get(name=language_dc.name)

            self.assertEqual(language_dc.name, language.name)
            self.assertEqual(language_dc.icon, language.icon)
            self.assertEqual(language_dc.proficiency, language.proficiency)
            self.assertEqual(language_dc.row, language.row)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        languages: list[Language] = (
            self.model.apps.get_model("resume", "Language").objects.all().values()
        )

        language_model = Language()
        language_model.clean(languages)

        for language in languages:
            self.assertIsNone(language.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        language_model: Any = self.model.apps.get_model("resume", "Language")

        language = Language()
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
