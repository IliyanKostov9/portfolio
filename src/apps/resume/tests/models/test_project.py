from typing import Any

from apps.resume.data_class.portfolio.project import Project as ProjectDataClass
from apps.resume.models.project import Project
from apps.resume.tests.models.portfolio import Portfolio


class ProjectTestCase(Portfolio):
    def test_from_yaml(self):
        self.setUp()

        project_model: Any = self.model.apps.get_model("resume", "Project")

        projects_dc: list[Any] = ProjectDataClass.from_yaml("portfolio/project.yaml")

        for project_dc in projects_dc:
            project: Project = project_model.objects.get(name=project_dc.name)

            self.assertEqual(project_dc.name, project.name)
            self.assertEqual(project_dc.description, project.description)
            self.assertEqual(project_dc.scroll_description, project.scroll_description)
            self.assertEqual(project_dc.image, project.image)
            self.assertEqual(project_dc.date, project.date)
            self.assertEqual(project_dc.row, project.row)
            self.assertEqual(project_dc.repositories, project.repositories)

        super().tearDownClass()

    def test_clean(self):
        self.setUp()

        projects: list[Project] = (
            self.model.apps.get_model("resume", "Project").objects.all().values()
        )

        project_model = Project()
        project_model.clean(projects)

        for project in projects:
            self.assertIsNone(project.get("id"), True)

        super().tearDownClass()

    def test_transform(self):
        self.setUp()
        project_model: Any = self.model.apps.get_model("resume", "Project")

        project = Project()
        project_transformed = project.transform()

        for projs in project_transformed:
            self.assertTrue(projs.get("row"))
            self.assertTrue(projs.get("project"))

            for proj in projs["project"]:
                proj_model = project_model.objects.get(name=proj["name"])

                self.assertEqual(proj_model.description, proj["description"])
                self.assertEqual(
                    proj_model.scroll_description, proj["scroll_description"]
                )
                self.assertEqual(proj_model.image, proj["image"])
                self.assertEqual(proj_model.date, proj["date"])
                self.assertEqual(proj_model.repositories, proj["repositories"])

        super().tearDownClass()
