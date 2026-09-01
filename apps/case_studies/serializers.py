from rest_framework import serializers
from .models import CaseStudy


class CaseStudyListSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(read_only=True)
    sourceUrl = serializers.URLField(source="source_url")
    myRole = serializers.CharField(source="my_role")

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "slug",
            "title",
            "date",
            "description",
            "tags",
            "sourceUrl",
            "featured",
            "banner",
            "problem",
            "architecture",
            "myRole",
            "outcome",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class CaseStudyDetailSerializer(CaseStudyListSerializer):
    class Meta(CaseStudyListSerializer.Meta):
        pass


class CaseStudyWriteSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(required=True)

    class Meta:
        model = CaseStudy
        fields = [
            "slug",
            "title",
            "date",
            "description",
            "tags",
            "source_url",
            "featured",
            "banner",
            "problem",
            "architecture",
            "my_role",
            "outcome",
        ]
        extra_kwargs = {
            "slug": {"required": False},
        }
