from django.db import models


class Lead(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новий"
        IN_PROGRESS = "in_progress", "В роботі"
        DONE = "done", "Завершено"
        SPAM = "spam", "Спам"

    class ProjectType(models.TextChoices):
        ECOMMERCE = "ecommerce", "Інтернет-магазин"
        LANDING = "landing", "Лендінг"
        CORPORATE = "corporate", "Корпоративний сайт"
        OTHER = "other", "Інше"

    name = models.CharField("Ім'я", max_length=120)
    contact = models.CharField("Телефон", max_length=200)
    project_type = models.CharField(
        "Тип проєкту",
        max_length=20,
        choices=ProjectType.choices,
        default=ProjectType.OTHER,
        blank=True,
    )
    comment = models.TextField("Коментар", blank=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    utm_source = models.CharField("UTM source", max_length=200, blank=True)
    utm_medium = models.CharField("UTM medium", max_length=200, blank=True)
    utm_campaign = models.CharField("UTM campaign", max_length=200, blank=True)
    source_url = models.URLField("URL джерела", blank=True)
    quiz_features = models.TextField("Функціонал (квіз)", blank=True)
    quiz_pages = models.CharField("Кількість сторінок (квіз)", max_length=20, blank=True)
    quiz_deadline = models.CharField("Терміни (квіз)", max_length=30, blank=True)
    quiz_budget = models.CharField("Бюджет (квіз)", max_length=30, blank=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_project_type_display()}"
