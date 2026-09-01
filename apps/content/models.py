from django.db import models


class SiteSettings(models.Model):
    name = models.CharField(max_length=200, blank=True, default="")
    footer_tagline = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"
