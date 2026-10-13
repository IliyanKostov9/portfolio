from typing import override

from django.views.generic import TemplateView


class Error404(TemplateView):
    template_name = "pages/error/404.html"

    @override
    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = 404
        return super().render_to_response(context, **response_kwargs)
