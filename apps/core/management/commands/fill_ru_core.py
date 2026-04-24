"""
Management command to populate Russian (_ru) translation fields
for Testimonial and PortfolioItem models.

Usage: python manage.py fill_ru_core
"""
from django.core.management.base import BaseCommand

from apps.core.models import PortfolioItem, Testimonial


TESTIMONIALS_RU = {
    "Олексій Петренко": {
        "name_ru": "Алексей Петренко",
        "company_ru": "ShopUA",
        "text_ru": (
            "Заказывали интернет-магазин — результат превзошёл ожидания. "
            "Сайт работает молниеносно, админка понятна даже менеджерам "
            "без технического опыта. Конверсия выросла на 40% по сравнению "
            "со старым сайтом на конструкторе."
        ),
    },
    "Марина Ковальчук": {
        "name_ru": "Марина Ковальчук",
        "company_ru": "DigitalPro Agency",
        "text_ru": (
            "Работаем с DOuIT уже над третьим проектом. Лендинги, которые они делают, "
            "загружаются мгновенно и конвертируют лучше любого Tilda-шаблона. "
            "Отдельный плюс — полный контроль над аналитикой и UTM."
        ),
    },
    "Ігор Савченко": {
        "name_ru": "Игорь Савченко",
        "company_ru": "ООО «Будсервис»",
        "text_ru": (
            "Корпоративный сайт сделали за 3 недели. Дизайн современный, "
            "админка на русском — наш маркетолог сам обновляет новости "
            "и услуги. Рекомендую всем, кто хочет качественный сайт без лишних платежей."
        ),
    },
    "Катерина Бондар": {
        "name_ru": "Екатерина Бондарь",
        "company_ru": "Цветочный дом",
        "text_ru": (
            "Наконец-то у нас магазин, который не тормозит! Раньше на Prom.ua "
            "клиенты уходили из-за медленной загрузки. Сейчас — быстро, красиво, "
            "и главное — никаких ежемесячных платежей за платформу."
        ),
    },
}


class Command(BaseCommand):
    help = "Fill _ru translation fields for Testimonial and PortfolioItem"

    def handle(self, *args, **options):
        updated_t = 0
        for name, data in TESTIMONIALS_RU.items():
            try:
                t = Testimonial.objects.get(name=name)
            except Testimonial.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Testimonial '{name}' not found, skipped"))
                continue
            for k, v in data.items():
                setattr(t, k, v)
            t.save(update_fields=list(data.keys()))
            updated_t += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {updated_t} testimonials"))

        updated_p = 0
        for p in PortfolioItem.objects.all():
            if not p.title_ru:
                p.title_ru = p.title
            if not p.description_ru:
                p.description_ru = p.description
            p.save(update_fields=["title_ru", "description_ru"])
            updated_p += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Touched {updated_p} portfolio items (manual RU fill recommended in admin)"
            )
        )
