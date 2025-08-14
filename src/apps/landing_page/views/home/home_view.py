from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View
from landing_page.models.technology import Technology


class HomeView(View):
    def get(self, request: Any) -> HttpResponse:
        template = loader.get_template("pages/home/index.html")

        technologies = self._get_technologies()
        print(technologies)

        context: dict[str, Any] = {"technologies": technologies}

        return HttpResponse(template.render(context, request))

    def _get_technologies(self) -> Any:
        technologies_objs = Technology.objects.all().values()

        technology_categories = set(item["category_id"] for item in technologies_objs)
        technologies = [
            {"name": name, "technologies": []} for name in technology_categories
        ]

        for category in technology_categories:
            index = next(
                (
                    index
                    for index, dic in enumerate(technologies)
                    if dic["name"] == category
                ),
                None,
            )

            technologies[index]["technologies"] = [
                item for item in technologies_objs if item["category_id"] == category
            ]

        # NOTE: Clean the elements in a dictionary with unnacessary id and category_id
        for category in technologies:
            for technology in category["technologies"]:
                print("technology")
                technology.pop("id")
                technology.pop("category_id")

        return technologies
