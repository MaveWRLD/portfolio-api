from rest_framework import serializers
from .models import CaseStudy


class CaseStudyImageSerializer(serializers.Serializer):
    src = serializers.URLField()
    aspect = serializers.FloatField()


class CaseStudyListSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(read_only=True)
    gallery = CaseStudyImageSerializer(many=True, read_only=True)
    display_title = serializers.CharField(read_only=True)

    class Meta:
        model = CaseStudy
        fields = [
            "id",
            "slug",
            "category",
            "date",
            "title",
            "display_title",
            "budget",
            "client",
            "tool",
            "featured",
            "banner",
            "gallery",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class CaseStudyDetailSerializer(CaseStudyListSerializer):
    class Meta(CaseStudyListSerializer.Meta):
        pass


class CaseStudyWriteSerializer(serializers.ModelSerializer):
    banner = serializers.ImageField(required=True)
    gallery = CaseStudyImageSerializer(many=True, required=False, default=list)

    class Meta:
        model = CaseStudy
        fields = [
            "slug",
            "category",
            "date",
            "title",
            "detail_title",
            "budget",
            "client",
            "tool",
            "featured",
            "banner",
            "gallery",
        ]
        extra_kwargs = {
            "slug": {"required": False},
        }

    def validate_gallery(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Gallery must be a list of objects.")
        for item in value:
            if not isinstance(item, dict) or "src" not in item or "aspect" not in item:
                raise serializers.ValidationError("Each gallery item must have 'src' and 'aspect'.")
        return value