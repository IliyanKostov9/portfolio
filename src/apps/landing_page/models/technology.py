from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Model
from landing_page.models.technology_category import TechnologyCategory


class Technology(Model):
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
