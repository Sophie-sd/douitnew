from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField("Назва сайту", max_length=100, default="DOuIT")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    email = models.EmailField("Email")
    telegram_url = models.URLField("Telegram URL", blank=True)
    whatsapp_url = models.URLField("WhatsApp URL", blank=True)
    og_image = models.ImageField(
        "OG-зображення", upload_to="og/", blank=True
    )

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Testimonial(models.Model):
    name = models.CharField("Ім'я", max_length=120)
    company = models.CharField("Компанія", max_length=120, blank=True)
    text = models.TextField("Відгук")
    rating = models.PositiveSmallIntegerField(
        "Рейтинг",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_active = models.BooleanField("Активний", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} — {self.company}" if self.company else self.name


class PortfolioItem(models.Model):
    title = models.CharField("Назва", max_length=200)
    url = models.URLField("URL проєкту", blank=True)
    screenshot = models.ImageField("Скріншот", upload_to="portfolio/")
    description = models.TextField("Опис", max_length=300)
    service_type = models.ForeignKey(
        "services.ServicePage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Тип послуги",
        related_name="portfolio_items",
    )
    is_active = models.BooleanField("Активний", default=True)
    order = models.PositiveSmallIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        verbose_name = "Робота в портфоліо"
        verbose_name_plural = "Портфоліо"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title
