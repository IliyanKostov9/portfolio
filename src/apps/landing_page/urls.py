from django.urls import path

from apps.landing_page.views.home.contact_me_view import ContactMeView
from apps.landing_page.views.home.home_view import HomeView
from apps.landing_page.views.monitor.csp_report_view import CSPReportView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home/contact-me/", ContactMeView.as_view(), name="home/contact-me"),
    path("csp-report/", CSPReportView.as_view(), name="monitor/csp-report"),
]
