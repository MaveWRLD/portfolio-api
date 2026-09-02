from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "featured", "created_at"]
    list_filter = ["featured", "date"]
    search_fields = ["title", "slug"]
    list_per_page = 20
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "date")}),
        ("Details", {"fields": ("description", "tags", "source_url", "featured")}),
        ("Case study", {"fields": ("problem", "architecture", "my_role", "outcome")}),
        ("Media", {"fields": ("banner",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
