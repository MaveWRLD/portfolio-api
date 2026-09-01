from django.db import models


class SiteSettings(models.Model):
    name = models.CharField(max_length=200, blank=True, default="")
    footer_tagline = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"


def hero_photo_upload_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"hero/photo.{ext}"


class HeroSection(models.Model):
    eyebrow = models.CharField(max_length=200, blank=True, default="")
    headline = models.CharField(max_length=300, blank=True, default="")
    subheading = models.CharField(max_length=500, blank=True, default="")
    photo = models.ImageField(upload_to=hero_photo_upload_path, blank=True, default="")
    cv_url = models.URLField(blank=True, default="")
    github_url = models.URLField(blank=True, default="")
    linkedin_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Hero section"
        verbose_name_plural = "Hero section"

    def __str__(self):
        return "Hero section"


class BrandSection(models.Model):
    brands = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Brand section"
        verbose_name_plural = "Brand section"

    def __str__(self):
        return "Brand section"


class ContactSection(models.Model):
    caption = models.CharField(max_length=100, blank=True, default="")
    heading = models.CharField(max_length=300, blank=True, default="")
    body = models.TextField(blank=True, default="")
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")

    class Meta:
        verbose_name = "Contact section"
        verbose_name_plural = "Contact section"

    def __str__(self):
        return "Contact section"


class ExperienceSection(models.Model):
    heading = models.CharField(max_length=300, blank=True, default="")
    body = models.TextField(blank=True, default="")
    experiences = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Experience section"
        verbose_name_plural = "Experience section"

    def __str__(self):
        return "Experience section"
