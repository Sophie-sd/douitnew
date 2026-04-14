from django.conf import settings
from django.core.mail import send_mail


def send_lead_email(lead):
    subject = f"Нова заявка: {lead.name} — {lead.get_project_type_display()}"
    body_lines = [
        f"Ім'я: {lead.name}",
        f"Контакт: {lead.contact}",
        f"Тип проєкту: {lead.get_project_type_display()}",
        f"Коментар: {lead.comment or '—'}",
        "",
        f"UTM source: {lead.utm_source or '—'}",
        f"UTM medium: {lead.utm_medium or '—'}",
        f"UTM campaign: {lead.utm_campaign or '—'}",
        f"Сторінка: {lead.source_url or '—'}",
    ]
    send_mail(
        subject=subject,
        message="\n".join(body_lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=True,
    )
