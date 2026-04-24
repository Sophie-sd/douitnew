from django.utils.translation import gettext_lazy as _

QUIZ_FEATURES = {
    "admin": _("Адмінка"),
    "catalog": _("Каталог товарів"),
    "payment": _("Онлайн-оплата"),
    "crm": _("CRM інтеграція"),
    "multilang": _("Мультимовність"),
    "blog": _("Блог"),
    "forms": _("Форми заявок"),
    "other": _("Інше"),
}

QUIZ_PAGES = {
    "1-5": "1 – 5",
    "6-15": "6 – 15",
    "16-50": "16 – 50",
    "50+": "50+",
}

QUIZ_DEADLINE = {
    "2weeks": _("До 2 тижнів"),
    "2-4weeks": _("2 – 4 тижні"),
    "1-2months": _("1 – 2 місяці"),
    "no-rush": _("Не поспішаю"),
}

QUIZ_BUDGET = {
    "up-to-500": _("До $500"),
    "500-1500": "$500 – $1 500",
    "1500-3000": "$1 500 – $3 000",
    "3000+": "$3 000+",
    "need-estimate": _("Потрібна оцінка"),
}


def humanize_features(raw: str) -> str:
    if not raw:
        return ""
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return ", ".join(str(QUIZ_FEATURES.get(p, p)) for p in parts)


def humanize(raw: str, mapping: dict) -> str:
    if not raw:
        return ""
    return str(mapping.get(raw.strip(), raw))
