from django.contrib import admin
from .models import (
    SiteSettings, HeroSection, BrandSection, ContactSection, ExperienceSection, ProjectsSection,
    FunFactsSection,
)


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


@admin.register(BrandSection)
class BrandSectionAdmin(SingletonAdmin):
    list_display = ["__str__"]


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    list_display = ["heading", "email"]


@admin.register(ExperienceSection)
class ExperienceSectionAdmin(SingletonAdmin):
    list_display = ["heading"]


@admin.register(ProjectsSection)
class ProjectsSectionAdmin(SingletonAdmin):
    list_display = ["heading"]


@admin.register(FunFactsSection)
class FunFactsSectionAdmin(SingletonAdmin):
    list_display = ["heading"]
