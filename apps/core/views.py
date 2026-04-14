from django.shortcuts import render
from django.utils.translation import get_language, gettext_lazy as _
from django.views.generic import TemplateView

from apps.services.models import ServicePage
from apps.services.views import _apply_ru

from .models import PortfolioItem, Testimonial


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        services = list(ServicePage.objects.filter(is_active=True))
        if get_language() == "ru":
            for s in services:
                _apply_ru(s, [("h1", "h1_ru"), ("hero_subtitle", "hero_subtitle_ru")])
        ctx["services"] = services
        ctx["testimonials"] = Testimonial.objects.filter(is_active=True)
        ctx["portfolio"] = PortfolioItem.objects.filter(is_active=True)[:6]
        ctx["meta_title"] = _("Розробка сайтів на чистому коді | DOuIT")
        ctx["meta_description"] = _(
            "Кодописні сайти на Django з надзручною адмінкою українською. "
            "Інтернет-магазини, лендінги, корпоративні сайти — швидко, гнучко, надійно."
        )
        return ctx


def custom_404(request, exception):
    return render(request, "404.html", status=404)
