import logging
from typing import Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

CARDS_ENDPOINT = "/pipelines/cards"


def _build_manager_comment(lead) -> str:
    parts: list[str] = []
    if lead.comment:
        parts.append(lead.comment.strip())

    quiz_lines: list[str] = []
    if lead.quiz_features:
        quiz_lines.append(f"Функціонал: {lead.quiz_features}")
    if lead.quiz_pages:
        quiz_lines.append(f"Сторінок: {lead.quiz_pages}")
    if lead.quiz_deadline:
        quiz_lines.append(f"Терміни: {lead.quiz_deadline}")
    if lead.quiz_budget:
        quiz_lines.append(f"Бюджет: {lead.quiz_budget}")
    if quiz_lines:
        parts.append("— Квіз —\n" + "\n".join(quiz_lines))

    source_lines: list[str] = []
    if lead.source_url:
        source_lines.append(f"Сторінка: {lead.source_url}")
    if lead.utm_source:
        source_lines.append(f"UTM source: {lead.utm_source}")
    if lead.utm_medium:
        source_lines.append(f"UTM medium: {lead.utm_medium}")
    if lead.utm_campaign:
        source_lines.append(f"UTM campaign: {lead.utm_campaign}")
    if source_lines:
        parts.append("— Джерело —\n" + "\n".join(source_lines))

    return "\n\n".join(parts)


def _build_payload(lead) -> dict:
    title = f"DOuIT — {lead.name} ({lead.get_project_type_display()})"

    payload: dict = {
        "title": title,
        "pipeline_id": settings.KEYCRM_PIPELINE_ID,
        "contact": {
            "full_name": lead.name,
            "phone": lead.contact,
        },
    }

    if settings.KEYCRM_SOURCE_ID:
        payload["source_id"] = settings.KEYCRM_SOURCE_ID

    comment = _build_manager_comment(lead)
    if comment:
        payload["manager_comment"] = comment

    for field in ("utm_source", "utm_medium", "utm_campaign"):
        value = getattr(lead, field, "")
        if value:
            payload[field] = value

    return payload


def send_lead_to_keycrm(lead) -> Optional[str]:
    """Push a lead into KeyCRM pipeline as a new card.

    Returns the created card id (str) on success, None otherwise.
    Failures are logged but never raised — the form submit must keep working
    even if KeyCRM is down.
    """
    token = settings.KEYCRM_API_TOKEN
    pipeline_id = settings.KEYCRM_PIPELINE_ID

    if not token or not pipeline_id:
        logger.debug("KeyCRM disabled (missing token or pipeline_id), skipping lead pk=%s", lead.pk)
        return None

    url = f"{settings.KEYCRM_API_URL.rstrip('/')}{CARDS_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = _build_payload(lead)

    try:
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=settings.KEYCRM_TIMEOUT,
        )
    except requests.RequestException:
        logger.exception("KeyCRM request failed for lead pk=%s", lead.pk)
        return None

    if response.status_code >= 400:
        logger.error(
            "KeyCRM rejected lead pk=%s: status=%s body=%s",
            lead.pk,
            response.status_code,
            response.text[:500],
        )
        return None

    try:
        data = response.json()
    except ValueError:
        logger.exception("KeyCRM returned non-JSON for lead pk=%s", lead.pk)
        return None

    card_id = data.get("id") or data.get("data", {}).get("id")
    if card_id is None:
        logger.warning("KeyCRM response without card id for lead pk=%s: %s", lead.pk, data)
        return None

    return str(card_id)
