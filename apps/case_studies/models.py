import uuid
from django.db import models
from django.utils.text import slugify


def case_study_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"case_studies/{instance.slug or uuid.uuid4().hex[:8]}/banner.{ext}"


def gallery_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"case_studies/{instance.case_study.slug or uuid.uuid4().hex[:8]}/gallery/{uuid.uuid4().hex[:8]}.{ext}"


class CaseStudy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    date = models.DateField()
    title = models.CharField(max_length=200)
    detail_title = models.CharField(max_length=200, blank=True, default="")
    budget = models.CharField(max_length=50, blank=True, default="")
    client = models.CharField(max_length=100, blank=True, default="")
    tool = models.CharField(max_length=100, blank=True, default="")
    featured = models.BooleanField(default=False)
    banner = models.ImageField(upload_to=case_study_upload_path)
    gallery = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["-date"]),
            models.Index(fields=["featured"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def display_title(self):
        return self.detail_title or self.title