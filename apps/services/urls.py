from django.urls import path

from .views import ServiceDetailView

app_name = "services"

urlpatterns = [
    path(
        "internet-mahazyny/",
        ServiceDetailView.as_view(),
        kwargs={"slug": "internet-mahazyny"},
        name="ecommerce",
    ),
    path(
        "lendinhy/",
        ServiceDetailView.as_view(),
        kwargs={"slug": "lendinhy"},
        name="landing",
    ),
    path(
        "korporatyvni-saity/",
        ServiceDetailView.as_view(),
        kwargs={"slug": "korporatyvni-saity"},
        name="corporate",
    ),
]
