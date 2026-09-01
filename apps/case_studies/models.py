import uuid
from django.db import models
from django.utils.text import slugify


def case_study_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"case_studies/{instance.slug or uuid.uuid4().hex[:8]}/banner.{ext}"


class CaseStudy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField(blank=True, default="")
    tags = models.JSONField(default=list, blank=True)
    source_url = models.URLField(blank=True, default="")
    featured = models.BooleanField(default=False)
    banner = models.ImageField(upload_to=case_study_upload_path)
    problem = models.TextField(blank=True, default="")
    architecture = models.TextField(blank=True, default="")
    my_role = models.TextField(blank=True, default="")
    outcome = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name_plural = "case studies"
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
