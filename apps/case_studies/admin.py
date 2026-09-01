from django.contrib import admin
from .models import CaseStudy


@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "date", "featured", "client", "created_at"]
    list_filter = ["featured", "category", "date"]
    search_fields = ["title", "detail_title", "slug", "client", "tool"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "date")}),
        ("Details", {"fields": ("detail_title", "budget", "client", "tool", "featured")}),
        ("Media", {"fields": ("banner", "gallery")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )