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


@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    list_display = ("title", "service_type", "is_active", "order")
    list_filter = ("is_active", "service_type")
    list_editable = ("is_active", "order")
    search_fields = ("title",)
