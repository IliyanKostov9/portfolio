from django.views.generic import TemplateView


class Error404(TemplateView):
    template_name = "pages/error/404.html"
