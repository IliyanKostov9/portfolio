from typing import Any

from apps.resume.data_class.work_history import WorkHistory as WorkHistoryDataClass
from apps.resume.models.work_history import WorkHistory
from apps.resume.tests.models.portfolio import Portfolio


class WorkHistoryTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        work_history_model: Any = self.model.apps.get_model("resume", "WorkHistory")

        work_histories_dc: list[Any] = WorkHistoryDataClass.from_yaml(
            "work_history.yaml"
        )

        for work_history_dc in work_histories_dc:
            for lang in self.languages:
                work_history: WorkHistory = work_history_model.objects.get(
                    specialty=getattr(work_history_dc, lang + "_specialty"),
                    dates=work_history_dc.dates,
                )

                self.assertEqual(
                    work_history_dc.company_name, work_history.company_name
                )
                self.assertEqual(
                    work_history_dc.company_name_label, work_history.company_name_label
                )
                self.assertEqual(work_history_dc.image, work_history.image)
                self.assertEqual(
                    getattr(work_history_dc, lang + "_specialty"),
                    work_history.specialty,
                )
                self.assertEqual(
                    getattr(work_history_dc, lang + "_description"),
                    work_history.description,
                )

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        work_histories: list[WorkHistory] = (
            self.model.apps.get_model("resume", "WorkHistory").objects.all().values()
        )

        work_history = WorkHistory()
        work_history.clean(work_histories)

        for work_history in work_histories:
            self.assertIsNone(work_history.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        work_history_model: Any = self.model.apps.get_model("resume", "WorkHistory")

        work_history = WorkHistory()
        work_history_transformed = work_history.transform()

        for work in work_history_transformed:
            work_model = work_history_model.objects.get(description=work.description)

            self.assertEqual(work_model.company_name, work.company_name)
            self.assertEqual(work_model.company_name_label, work.company_name_label)
            self.assertEqual(work_model.image, work.image)
            self.assertEqual(work_model.specialty, work.specialty)
            self.assertEqual(work_model.description, work.description)

        super().tearDownClass()
