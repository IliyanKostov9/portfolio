"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.blogs.blog_sitemap import BlogSiteMap
from apps.resume.resume_sitemap import ResumeSiteMap
from portfolio.views.error.error_404 import Error404
from portfolio.views.error.error_500 import Error500
from portfolio.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    # path("admin/", admin.site.urls),  # pyre-ignore[16]
    path("i18n/", include("django.conf.urls.i18n")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"static": ResumeSiteMap, "blog": BlogSiteMap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("monitor/csp-report", CSPReportView.as_view(), name="csp-report"),
]

urlpatterns += i18n_patterns(
    path("", include("apps.resume.urls")),
    path("blogs/", include("apps.blogs.urls")),
)

handler404 = Error404.as_view()
handler500 = Error500.as_view()
