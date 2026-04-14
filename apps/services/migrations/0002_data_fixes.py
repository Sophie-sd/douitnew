from django.db import migrations


def apply_fixes(apps, schema_editor):
    ServicePage = apps.get_model("services", "ServicePage")
    Feature = apps.get_model("services", "Feature")
    FAQ = apps.get_model("services", "FAQ")

    # Ecommerce page
    ServicePage.objects.filter(slug="internet-mahazyny").update(
        price_from=750,
        hero_subtitle=(
            "Кодописний інтернет-магазин — без щомісячних платежів, "
            "з повним контролем над функціоналом та дизайном."
        ),
        meta_title="Інтернет-магазин на чистому коді від $750 | DOuIT",
        meta_description=(
            "Розробка інтернет-магазинів від $750. Без абонплати, "
            "з адмінкою українською, інтеграції з НП та LiqPay."
        ),
    )

    # Corporate page meta
    ServicePage.objects.filter(slug="korporatyvni-saity").update(
        meta_description=(
            "Розробка корпоративних сайтів від $450. "
            "Адмінка українською, SEO-оптимізація, мобільна адаптація."
        ),
    )

    # Corporate Feature "Безпека"
    Feature.objects.filter(
        page__slug="korporatyvni-saity",
        title="Безпека",
    ).update(text="Наш стек захищає від основних веб-вразливостей.")

    # Corporate FAQ "Чи можна додати блог?"
    FAQ.objects.filter(
        page__slug="korporatyvni-saity",
        question="Чи можна додати блог?",
    ).update(answer="Так, кодописне рішення дозволяє легко додати блог або новини.")


def reverse_fixes(apps, schema_editor):
    ServicePage = apps.get_model("services", "ServicePage")
    Feature = apps.get_model("services", "Feature")
    FAQ = apps.get_model("services", "FAQ")

    ServicePage.objects.filter(slug="internet-mahazyny").update(
        price_from=800,
        hero_subtitle=(
            "Кодописний інтернет-магазин на Django — без щомісячних платежів, "
            "з повним контролем над функціоналом та дизайном."
        ),
        meta_title="Інтернет-магазин на чистому коді від $800 | DOuIT",
        meta_description=(
            "Розробка інтернет-магазинів на Django від $800. Без абонплати, "
            "з адмінкою українською, інтеграції з НП та LiqPay."
        ),
    )

    ServicePage.objects.filter(slug="korporatyvni-saity").update(
        meta_description=(
            "Розробка корпоративних сайтів на Django від $450. "
            "Адмінка українською, SEO-оптимізація, мобільна адаптація."
        ),
    )

    Feature.objects.filter(
        page__slug="korporatyvni-saity",
        title="Безпека",
    ).update(text="Django захищає від основних веб-вразливостей.")

    FAQ.objects.filter(
        page__slug="korporatyvni-saity",
        question="Чи можна додати блог?",
    ).update(answer="Так, Django дозволяє легко додати блог або новини.")


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_fixes, reverse_fixes),
    ]
