from rest_framework import serializers
from .models import SiteSettings, HeroSection, BrandSection


class SiteSettingsSerializer(serializers.ModelSerializer):
    footerTagline = serializers.CharField(source="footer_tagline")

    class Meta:
        model = SiteSettings
        fields = ["name", "footerTagline"]


class HeroSectionSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(read_only=True, use_url=True, allow_null=True)
    cvUrl = serializers.URLField(source="cv_url")
    githubUrl = serializers.URLField(source="github_url")
    linkedinUrl = serializers.URLField(source="linkedin_url")

    class Meta:
        model = HeroSection
        fields = ["eyebrow", "headline", "subheading", "photo", "cvUrl", "githubUrl", "linkedinUrl"]


class BrandSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandSection
        fields = ["brands"]
