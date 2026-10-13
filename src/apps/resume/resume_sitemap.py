from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ResumeSiteMap(Sitemap):
    i18n = True
    languages = ["en", "bg", "fr", "de"]
    alternates = True
    x_default = True
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return ["resume:home", "blogs:blogs"]

    def location(self, item):
        return reverse(item)
