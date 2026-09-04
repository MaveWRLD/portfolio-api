from rest_framework import serializers
from .models import (
    SiteSettings, HeroSection, BrandSection, ContactSection, ExperienceSection, ProjectsSection,
    FunFactsSection, TickerSection, AboutSection, StackSection, Experience,
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


class ExperienceSerializer(serializers.ModelSerializer):
    period = serializers.CharField(source="period_display", read_only=True)

    class Meta:
        model = Experience
        fields = ["company", "role", "period"]


class ExperienceSectionSerializer(serializers.ModelSerializer):
    experiences = ExperienceSerializer(many=True, read_only=True)

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


class AboutSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutSection
        fields = ["heading", "body"]


class StackSectionSerializer(serializers.Serializer):
    languages = serializers.ListField(child=serializers.CharField())
    data = serializers.ListField(child=serializers.CharField())
    infra = serializers.ListField(child=serializers.CharField())

    def to_representation(self, instance):
        # Technology rows are grouped by category back into the
        # {languages, data, infra} shape the frontend already expects —
        # keeps that contract stable across the JSONField -> model swap.
        grouped = {"language": [], "data": [], "infra": []}
        for tech in instance.technologies.all():
            grouped.setdefault(tech.category, []).append(tech.name)
        return {
            "languages": grouped["language"],
            "data": grouped["data"],
            "infra": grouped["infra"],
        }
