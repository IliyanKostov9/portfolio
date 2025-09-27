from collections import defaultdict
from typing import Any

from django.db.models import CASCADE, CharField, ForeignKey, IntegerField
from typing_extensions import override

from apps.resume.models.portfolio import Portfolio
from apps.resume.models.technology_category import TechnologyCategory


class Technology(Portfolio):
    name: CharField = CharField("Name of the technology", max_length=50)
    icon: CharField = CharField("Icon name of the technology", max_length=20)
    row: IntegerField = IntegerField("Row number of the technology")
    page: IntegerField = IntegerField("Page number of the technology")
    category: ForeignKey = ForeignKey(
        TechnologyCategory,
        verbose_name="Category of the technology",
        on_delete=CASCADE,
    )
    # avatar = models.ImageField(name=f"{name}-avatar", width_field=300, height_field=300)

    @override
    def get_all(self) -> Any:
        return list(Technology.objects.all().values())

    @override
    def transform(self) -> Any:
        technologies_objs = self.get_all()
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

    @override
    def clean(self, technologies) -> None:
        for technology in technologies:
            technology.pop("id")
