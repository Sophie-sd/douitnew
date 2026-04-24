import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from . import quiz_labels

logger = logging.getLogger(__name__)


def send_lead_email(lead) -> None:
    subject = f"Нова заявка: {lead.name} — {lead.get_project_type_display()}"

    quiz_features_human = quiz_labels.humanize_features(lead.quiz_features)
    quiz_pages_human = quiz_labels.humanize(lead.quiz_pages, quiz_labels.QUIZ_PAGES)
    quiz_deadline_human = quiz_labels.humanize(lead.quiz_deadline, quiz_labels.QUIZ_DEADLINE)
    quiz_budget_human = quiz_labels.humanize(lead.quiz_budget, quiz_labels.QUIZ_BUDGET)

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
            f"Функціонал: {quiz_features_human or '—'}",
            f"Сторінок: {quiz_pages_human or '—'}",
            f"Терміни: {quiz_deadline_human or '—'}",
            f"Бюджет: {quiz_budget_human or '—'}",
            "",
        ]
    plain_lines += [
        "— Джерело —",
        f"Сторінка: {lead.source_url or '—'}",
        f"UTM source: {lead.utm_source or '—'}",
        f"UTM medium: {lead.utm_medium or '—'}",
        f"UTM campaign: {lead.utm_campaign or '—'}",
    ]

    html_body = render_to_string(
        "leads/email/lead_notification.html",
        {
            "lead": lead,
            "quiz_features_human": quiz_features_human,
            "quiz_pages_human": quiz_pages_human,
            "quiz_deadline_human": quiz_deadline_human,
            "quiz_budget_human": quiz_budget_human,
        },
    )

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
