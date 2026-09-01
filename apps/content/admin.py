from django.contrib import admin
from .models import SiteSettings, HeroSection


class SingletonAdmin(admin.ModelAdmin):
    """Prevents adding a second row or deleting the only row."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    list_display = ["name", "footer_tagline"]


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    list_display = ["headline", "eyebrow"]
