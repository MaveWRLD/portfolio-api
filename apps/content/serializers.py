from rest_framework import serializers
from .models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    footerTagline = serializers.CharField(source="footer_tagline")

    class Meta:
        model = SiteSettings
        fields = ["name", "footerTagline"]
