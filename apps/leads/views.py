from django.core.cache import cache
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import LeadForm, ModalLeadForm
from .notifications import send_lead_email


class ThankYouView(TemplateView):
    template_name = "leads/thank_you.html"


class QuizPageView(TemplateView):
    template_name = "leads/quiz_page.html"


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _is_rate_limited(request, max_requests=3, window=600):
    ip = _get_client_ip(request)
    key = f"lead_rate_{ip}"
    count = cache.get(key, 0)
    if count >= max_requests:
        return True
    cache.set(key, count + 1, window)
    return False


def _save_lead(form):
    lead = form.save(commit=False)
    cd = form.cleaned_data
    lead.utm_source = cd.get("utm_source", "")
    lead.utm_medium = cd.get("utm_medium", "")
    lead.utm_campaign = cd.get("utm_campaign", "")
    lead.source_url = cd.get("source_url", "")
    lead.quiz_features = cd.get("quiz_features", "")
    lead.quiz_pages = cd.get("quiz_pages", "")
    lead.quiz_deadline = cd.get("quiz_deadline", "")
    lead.quiz_budget = cd.get("quiz_budget", "")
    lead.save()
    send_lead_email(lead)
    return lead


def _redirect_thank_you():
    resp = HttpResponse(status=200)
    resp["HX-Redirect"] = reverse("leads:thank_you")
    return resp


@require_POST
def submit_lead(request):
    if not request.headers.get("HX-Request"):
        return HttpResponse(status=400)

    hide_project_type = "project_type" not in request.POST

    if _is_rate_limited(request):
        return HttpResponse(
            render_to_string("components/lead_form.html", {
                "form": LeadForm(),
                "rate_limited": True,
                "hide_project_type": hide_project_type,
            }, request=request)
        )

    form = LeadForm(request.POST)
    if form.is_valid():
        if not form.cleaned_data.get("website"):
            _save_lead(form)
        return _redirect_thank_you()

    return HttpResponse(
        render_to_string("components/lead_form.html", {
            "form": form,
            "hide_project_type": hide_project_type,
        }, request=request)
    )


@require_POST
def submit_modal(request):
    if not request.headers.get("HX-Request"):
        return HttpResponse(status=400)

    if _is_rate_limited(request):
        return HttpResponse(
            render_to_string("components/quiz_contact_step.html", {
                "form": ModalLeadForm(),
                "rate_limited": True,
            }, request=request)
        )

    form = ModalLeadForm(request.POST)
    if form.is_valid():
        if form.cleaned_data.get("website"):
            return _redirect_thank_you()
        _save_lead(form)
        return _redirect_thank_you()

    return HttpResponse(
        render_to_string("components/quiz_contact_step.html", {"form": form}, request=request)
    )
