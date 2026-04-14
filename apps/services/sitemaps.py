from django.contrib.sitemaps import Sitemap

from .models import ServicePage


class ServiceSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ServicePage.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()
