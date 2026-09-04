from django import forms
from django.contrib import admin
from .models import (
    SiteSettings, HeroSection, BrandSection, ContactSection, ExperienceSection, ProjectsSection,
    FunFactsSection, TickerSection, AboutSection, StackSection, Experience, Technology,
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


class HeroSectionForm(forms.ModelForm):
    # photo_data is a BinaryField (not directly form-editable), so this
    # unbound upload field feeds save_model below instead.
    photo_upload = forms.ImageField(required=False, label="Photo")

    class Meta:
        model = HeroSection
        exclude = ["photo_data", "photo_content_type", "photo_filename"]


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    form = HeroSectionForm
    list_display = ["headline", "eyebrow"]

    def save_model(self, request, obj, form, change):
        upload = form.cleaned_data.get("photo_upload")
        if upload:
            obj.photo_data = upload.read()
            obj.photo_content_type = upload.content_type or "application/octet-stream"
            obj.photo_filename = upload.name
        super().save_model(request, obj, form, change)


@admin.register(BrandSection)
class BrandSectionAdmin(SingletonAdmin):
    list_display = ["__str__"]


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    list_display = ["heading", "email"]


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1
    fields = ("role", "company", "start_date", "end_date", "order")
    ordering = ("order",)


@admin.register(ExperienceSection)
class ExperienceSectionAdmin(SingletonAdmin):
    list_display = ["heading"]
    inlines = [ExperienceInline]


@admin.register(ProjectsSection)
class ProjectsSectionAdmin(SingletonAdmin):
    list_display = ["heading"]


@admin.register(FunFactsSection)
class FunFactsSectionAdmin(SingletonAdmin):
    list_display = ["heading"]


@admin.register(TickerSection)
class TickerSectionAdmin(SingletonAdmin):
    list_display = ["__str__"]


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    list_display = ["heading"]


class TechnologyInline(admin.TabularInline):
    model = Technology
    extra = 1
    fields = ("name", "category", "icon", "order")
    ordering = ("category", "order")


@admin.register(StackSection)
class StackSectionAdmin(SingletonAdmin):
    list_display = ["__str__"]
    inlines = [TechnologyInline]
