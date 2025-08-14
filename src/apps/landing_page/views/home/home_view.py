from collections import defaultdict
from typing import Any

from django.http import HttpResponse
from django.template import loader
from django.views import View
from landing_page.models.technology import Technology


class HomeView(View):
    def get(self, request: Any) -> HttpResponse:
        template = loader.get_template("pages/home/index.html")
        technologies = self._get_technologies()

        context: dict[str, Any] = {"technologies": technologies}

        return HttpResponse(template.render(context, request))

    def _get_technologies(self) -> Any:
        technologies_objs = list(Technology.objects.all().values())
        pages = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for tech in technologies_objs:
            page = tech["page"]
            category = tech["category_id"]
            row = tech["row"]

            item_data = {
                k: v for k, v in tech.items() if k not in ("page", "row", "category_id")
            }
            pages[page][category][row].append(item_data)

        def dictify(obj):
            if isinstance(obj, defaultdict):
                return {k: dictify(v) for k, v in obj.items()}
            elif isinstance(obj, dict):
                return {k: dictify(v) for k, v in obj.items()}
            return obj

        pages_clean = dictify(pages)

        result = {
            "pages": {
                page: {
                    "categories": {
                        category: {"rows": rows}
                        for category, rows in categories.items()
                    }
                }
                for page, categories in pages_clean.items()
            }
        }

        # TODO: Clean the elements in a dictionary with unnacessary id and category_id
        return result
