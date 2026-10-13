from typing import override

from django.views.generic import TemplateView


class Error500(TemplateView):
    template_name = "pages/error/500.html"

    @override
    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = 500
        return super().render_to_response(context, **response_kwargs)
