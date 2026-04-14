from django.conf import settings as django_settings

from .models import SiteSettings


def site_settings(request):
    try:
        site = SiteSettings.load()
    except Exception:
        site = None
    return {
        "site_settings": site,
        "gtm_id": django_settings.GTM_ID,
    }
