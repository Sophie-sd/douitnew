from django.contrib import admin

from .models import FAQ, Feature, ServicePage


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1
    fields = ("order", "icon_name", "title", "text", "title_ru", "text_ru")


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ("order", "question", "answer", "question_ru", "answer_ru")


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ("h1", "slug", "price_from", "is_active")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("h1",)}
    inlines = [FeatureInline, FAQInline]

    fieldsets = (
        (None, {
            "fields": ("slug", "is_active", "price_from", "price_currency"),
        }),
        ("Контент (UA)", {
            "fields": ("h1", "hero_subtitle", "meta_title", "meta_description", "body_intro", "process_steps"),
        }),
        ("Переклад (RU)", {
            "classes": ("collapse",),
            "fields": ("h1_ru", "hero_subtitle_ru", "meta_title_ru", "meta_description_ru", "body_intro_ru", "process_steps_ru"),
        }),
    )
