import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact",
        "project_type",
        "status",
        "utm_source",
        "created_at",
    )
    list_filter = ("status", "project_type", "created_at")
    search_fields = ("name", "contact")
    list_editable = ("status",)
    readonly_fields = (
        "utm_source",
        "utm_medium",
        "utm_campaign",
        "source_url",
        "quiz_features",
        "quiz_pages",
        "quiz_deadline",
        "quiz_budget",
        "created_at",
        "updated_at",
    )
    actions = ["export_csv"]

    @admin.action(description="Експорт у CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="leads.csv"'
        response.write("\ufeff")
        writer = csv.writer(response)
        writer.writerow(
            [
                "Ім'я",
                "Контакт",
                "Тип",
                "Коментар",
                "Функціонал",
                "Сторінки",
                "Терміни",
                "Бюджет",
                "Статус",
                "UTM source",
                "UTM medium",
                "UTM campaign",
                "URL",
                "Створено",
            ]
        )
        for lead in queryset:
            writer.writerow(
                [
                    lead.name,
                    lead.contact,
                    lead.get_project_type_display(),
                    lead.comment,
                    lead.quiz_features,
                    lead.quiz_pages,
                    lead.quiz_deadline,
                    lead.quiz_budget,
                    lead.get_status_display(),
                    lead.utm_source,
                    lead.utm_medium,
                    lead.utm_campaign,
                    lead.source_url,
                    lead.created_at.strftime("%Y-%m-%d %H:%M"),
                ]
            )
        return response
