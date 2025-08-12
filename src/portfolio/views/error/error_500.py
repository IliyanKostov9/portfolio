from django.views.generic import TemplateView


class Error500(TemplateView):
    template_name = "pages/error/500.html"
