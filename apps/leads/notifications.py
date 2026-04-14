import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_lead_email(lead) -> None:
    subject = f"Нова заявка: {lead.name} — {lead.get_project_type_display()}"

    plain_lines = [
        f"Ім'я: {lead.name}",
        f"Контакт: {lead.contact}",
        f"Тип проєкту: {lead.get_project_type_display()}",
        f"Коментар: {lead.comment or '—'}",
        "",
    ]
    if any([lead.quiz_features, lead.quiz_pages, lead.quiz_deadline, lead.quiz_budget]):
        plain_lines += [
            "— Квіз —",
            f"Функціонал: {lead.quiz_features or '—'}",
            f"Сторінок: {lead.quiz_pages or '—'}",
            f"Терміни: {lead.quiz_deadline or '—'}",
            f"Бюджет: {lead.quiz_budget or '—'}",
            "",
        ]
    plain_lines += [
        "— Джерело —",
        f"Сторінка: {lead.source_url or '—'}",
        f"UTM source: {lead.utm_source or '—'}",
        f"UTM medium: {lead.utm_medium or '—'}",
        f"UTM campaign: {lead.utm_campaign or '—'}",
    ]

    html_body = render_to_string("leads/email/lead_notification.html", {"lead": lead})

    msg = EmailMultiAlternatives(
        subject=subject,
        body="\n".join(plain_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL],
    )
    msg.attach_alternative(html_body, "text/html")

    try:
        msg.send()
    except Exception:
        logger.exception("Failed to send lead email for lead pk=%s", lead.pk)
