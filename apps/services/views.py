import json

from django.shortcuts import get_object_or_404
from django.utils.translation import get_language, gettext as _
from django.views.generic import DetailView

from .models import ServicePage


TEMPLATE_MAP = {
    "internet-mahazyny": "services/ecommerce.html",
    "lendinhy": "services/landing.html",
    "korporatyvni-saity": "services/corporate.html",
}


def _apply_ru(obj, field_pairs):
    """Replace Ukrainian field values with Russian ones in-memory (no DB write)."""
    for uk_field, ru_field in field_pairs:
        ru_val = getattr(obj, ru_field, None)
        if ru_val:
            setattr(obj, uk_field, ru_val)


class ServiceDetailView(DetailView):
    model = ServicePage
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_template_names(self):
        return [TEMPLATE_MAP.get(self.object.slug, "services/_base.html")]

    def get_object(self, queryset=None):
        return get_object_or_404(
            ServicePage, slug=self.kwargs["slug"], is_active=True
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.object
        features = list(page.features.all())
        faqs = list(page.faqs.all())

        if get_language() == "ru":
            _apply_ru(page, [
                ("h1", "h1_ru"),
                ("hero_subtitle", "hero_subtitle_ru"),
                ("body_intro", "body_intro_ru"),
                ("process_steps", "process_steps_ru"),
            ])
            ctx["meta_title"] = page.meta_title_ru or page.meta_title
            ctx["meta_description"] = page.meta_description_ru or page.meta_description
            for feature in features:
                _apply_ru(feature, [("title", "title_ru"), ("text", "text_ru")])
            for faq in faqs:
                _apply_ru(faq, [("question", "question_ru"), ("answer", "answer_ru")])
        else:
            ctx["meta_title"] = page.meta_title
            ctx["meta_description"] = page.meta_description

        ctx["features"] = features
        ctx["faqs"] = faqs
        ctx["faqs_json_ld"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq.question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq.answer,
                        },
                    }
                    for faq in faqs
                ],
            },
            ensure_ascii=False,
        )
        ctx["service_json_ld"] = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": page.h1,
                "description": ctx["meta_description"],
                "provider": {
                    "@type": "Organization",
                    "name": "DOuIT",
                },
                "offers": {
                    "@type": "Offer",
                    "price": str(page.price_from),
                    "priceCurrency": "USD",
                    "priceSpecification": {
                        "@type": "PriceSpecification",
                        "price": str(page.price_from),
                        "priceCurrency": "USD",
                        "description": f"{_('від')} {page.price_currency}{page.price_from}",
                    },
                },
            },
            ensure_ascii=False,
        )
        return ctx
