from django.contrib import admin

from .models import PortfolioItem, SiteSettings, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "phone", "email")

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "rating", "is_active", "order")
    list_filter = ("is_active", "rating")
    list_editable = ("is_active", "order")
    search_fields = ("name", "company")
    fieldsets = (
        (None, {"fields": ("name", "company", "text", "rating", "is_active", "order")}),
        ("Russian / Русский", {"fields": ("name_ru", "company_ru", "text_ru"), "classes": ("collapse",)}),
    )


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "service_type", "is_active", "order")
    list_filter = ("is_active", "service_type")
    list_editable = ("is_active", "order")
    search_fields = ("title",)
    fieldsets = (
        (None, {"fields": ("title", "url", "screenshot", "description", "service_type", "is_active", "order")}),
        ("Russian / Русский", {"fields": ("title_ru", "description_ru"), "classes": ("collapse",)}),
    )
