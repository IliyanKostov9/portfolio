from typing import Any

from django.db.models import CharField
from django.utils.translation import gettext as _
from parler.models import TranslatedFields
from typing_extensions import override

from apps.resume.models.portfolio_translate import PortfolioTranslate


class TechnologyCategory(PortfolioTranslate):
    translations: TranslatedFields = TranslatedFields(
        name=CharField(_("name"), max_length=50, primary_key=True)
    )

    @override
    def get_all(self) -> Any:
        return list(TechnologyCategory.objects.all().values())

    @override
    def transform(self) -> Any:
        pass

    @override
    def clean(self) -> None:
        pass

    def __unicode__(self):
        return self.name
