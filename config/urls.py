from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

from apps.core.sitemaps import StaticViewSitemap
from apps.services.sitemaps import ServiceSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    *i18n_patterns(
        path("dyakuyemo/", RedirectView.as_view(pattern_name="leads:thank_you", permanent=True)),
        path("rozrahunok/", RedirectView.as_view(pattern_name="leads:quiz_page", permanent=True)),
        path("leads/", include("apps.leads.urls")),
        path("", include("apps.services.urls")),
        path("", include("apps.core.urls")),
        prefix_default_language=False,
    ),
]

handler404 = "apps.core.views.custom_404"
