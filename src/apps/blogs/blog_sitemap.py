from django.contrib.sitemaps import Sitemap
from django.utils.translation import override

from apps.blogs.models.blog import Blog


class BlogSiteMap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        with override(obj.language.language):
            return obj.get_absolute_url()
