from django.db import models
from django.urls import reverse

_SLUG_TO_URL = {
    "internet-mahazyny": "services:ecommerce",
    "lendinhy": "services:landing",
    "korporatyvni-saity": "services:corporate",
}


class ServicePage(models.Model):
    SLUG_CHOICES = [
        ("internet-mahazyny", "Інтернет-магазини"),
        ("lendinhy", "Лендінги"),
        ("korporatyvni-saity", "Корпоративні сайти"),
    ]

    slug = models.SlugField("Slug", unique=True, choices=SLUG_CHOICES)

    # Ukrainian (primary)
    h1 = models.CharField("H1 заголовок", max_length=200)
    hero_subtitle = models.TextField("Підзаголовок hero")
    meta_title = models.CharField("Meta title", max_length=70)
    meta_description = models.CharField("Meta description", max_length=160)
    price_from = models.DecimalField("Ціна від", max_digits=8, decimal_places=0)
    price_currency = models.CharField("Валюта", max_length=5, default="$")
    body_intro = models.TextField("Вступний текст", blank=True)
    process_steps = models.JSONField(
        "Етапи роботи",
        default=list,
        blank=True,
        help_text='JSON: [{"title": "...", "text": "..."}]',
    )
    is_active = models.BooleanField("Активна", default=True)

    # Russian translations
    h1_ru = models.CharField("H1 (RU)", max_length=200, blank=True)
    hero_subtitle_ru = models.TextField("Підзаголовок hero (RU)", blank=True)
    meta_title_ru = models.CharField("Meta title (RU)", max_length=70, blank=True)
    meta_description_ru = models.CharField("Meta description (RU)", max_length=160, blank=True)
    body_intro_ru = models.TextField("Вступний текст (RU)", blank=True)
    process_steps_ru = models.JSONField(
        "Етапи роботи (RU)",
        default=list,
        blank=True,
        help_text='JSON: [{"title": "...", "text": "..."}]',
    )

    class Meta:
        verbose_name = "Сторінка послуги"
        verbose_name_plural = "Сторінки послуг"

    def __str__(self):
        return self.h1

    def get_absolute_url(self):
        return reverse(_SLUG_TO_URL[self.slug])


class Feature(models.Model):
    page = models.ForeignKey(
        ServicePage,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Послуга",
    )
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    icon_name = models.CharField("Іконка (CSS-клас)", max_length=60, blank=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    # Russian translations
    title_ru = models.CharField("Заголовок (RU)", max_length=200, blank=True)
    text_ru = models.TextField("Текст (RU)", blank=True)

    class Meta:
        verbose_name = "Перевага"
        verbose_name_plural = "Переваги"
        ordering = ["order"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    page = models.ForeignKey(
        ServicePage,
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name="Послуга",
    )
    question = models.CharField("Питання", max_length=300)
    answer = models.TextField("Відповідь")
    order = models.PositiveSmallIntegerField("Порядок", default=0)

    # Russian translations
    question_ru = models.CharField("Питання (RU)", max_length=300, blank=True)
    answer_ru = models.TextField("Відповідь (RU)", blank=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"
        ordering = ["order"]

    def __str__(self):
        return self.question
