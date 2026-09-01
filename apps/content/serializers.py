from rest_framework import serializers
from .models import (
    SiteSettings, HeroSection, BrandSection, ContactSection, ExperienceSection, ProjectsSection,
    FunFactsSection, TickerSection,
)


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


class ContactSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSection
        fields = ["caption", "heading", "body", "email", "phone"]


class ExperienceSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceSection
        fields = ["heading", "body", "experiences"]


class ProjectsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsSection
        fields = ["heading"]


class FunFactsSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunFactsSection
        fields = ["heading", "stats", "testimonials"]


class TickerSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerSection
        fields = ["phrases"]
