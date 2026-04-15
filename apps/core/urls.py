from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "publichnyi-dohovir/",
        TemplateView.as_view(template_name="legal/public_contract.html"),
        name="legal_public_contract",
    ),
    path(
        "polityka-konfidentsiinosti/",
        TemplateView.as_view(template_name="legal/privacy_policy.html"),
        name="legal_privacy",
    ),
    path(
        "polityka-cookies/",
        TemplateView.as_view(template_name="legal/cookie_policy.html"),
        name="legal_cookies",
    ),
    path(
        "polityka-povernennia/",
        TemplateView.as_view(template_name="legal/refund_policy.html"),
        name="legal_refund",
    ),
    path(
        "intelektualna-vlasnist/",
        TemplateView.as_view(template_name="legal/intellectual_property.html"),
        name="legal_ip",
    ),
]
