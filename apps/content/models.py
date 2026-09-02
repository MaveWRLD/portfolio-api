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

    class Meta:
        verbose_name = "Experience section"
        verbose_name_plural = "Experience section"

    def __str__(self):
        return "Experience section"


class Experience(models.Model):
    section = models.ForeignKey(ExperienceSection, related_name="experiences", on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null = "Present"
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    @property
    def period_display(self):
        start = self.start_date.strftime("%b %Y")
        end = self.end_date.strftime("%b %Y") if self.end_date else "Present"
        return f"{start} — {end}"


class ProjectsSection(models.Model):
    heading = models.CharField(max_length=300, blank=True, default="")

    class Meta:
        verbose_name = "Projects section"
        verbose_name_plural = "Projects section"

    def __str__(self):
        return "Projects section"


class FunFactsSection(models.Model):
    heading = models.CharField(max_length=300, blank=True, default="")
    stats = models.JSONField(default=list, blank=True)
    testimonials = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Fun facts section"
        verbose_name_plural = "Fun facts section"

    def __str__(self):
        return "Fun facts section"


class TickerSection(models.Model):
    phrases = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Ticker section"
        verbose_name_plural = "Ticker section"

    def __str__(self):
        return "Ticker section"


class AboutSection(models.Model):
    heading = models.CharField(max_length=200, blank=True, default="")
    body = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "About section"
        verbose_name_plural = "About section"

    def __str__(self):
        return "About section"


class StackSection(models.Model):
    class Meta:
        verbose_name = "Stack section"
        verbose_name_plural = "Stack section"

    def __str__(self):
        return "Stack section"


class Technology(models.Model):
    class Category(models.TextChoices):
        LANGUAGE = "language", "Language"
        DATA = "data", "Data"
        INFRA = "infra", "Infra"

    section = models.ForeignKey(StackSection, related_name="technologies", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    icon = models.CharField(max_length=100, blank=True, default="")  # optional: icon slug/url
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.category})"
