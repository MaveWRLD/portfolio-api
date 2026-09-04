import hashlib

from django.http import HttpResponse, HttpResponseNotModified, Http404
from rest_framework import generics
from rest_framework.views import APIView
from .models import (
    SiteSettings, HeroSection, BrandSection, ContactSection, ExperienceSection, ProjectsSection,
    FunFactsSection, TickerSection, AboutSection, StackSection,
)
from .serializers import (
    SiteSettingsSerializer, HeroSectionSerializer, BrandSectionSerializer, ContactSectionSerializer,
    ExperienceSectionSerializer, ProjectsSectionSerializer, FunFactsSectionSerializer,
    TickerSectionSerializer, AboutSectionSerializer, StackSectionSerializer,
)


class SingletonRetrieveAPIView(generics.RetrieveAPIView):
    """Base for a single-row content section. Auto-creates row pk=1 if
    missing so admin always has something to edit before content is seeded.
    """
    model = None

    def get_object(self):
        obj, _ = self.model.objects.get_or_create(pk=1)
        return obj


class SiteSettingsView(SingletonRetrieveAPIView):
    model = SiteSettings
    serializer_class = SiteSettingsSerializer


class HeroSectionView(SingletonRetrieveAPIView):
    model = HeroSection
    serializer_class = HeroSectionSerializer


class HeroPhotoView(APIView):
    """Serves the hero photo bytes straight from Postgres (photo_data).

    ETag is a hash of the bytes themselves, so it changes automatically
    whenever the admin swaps the photo — no manual cache purge needed for
    browser/CDN revalidation.
    """

    def get(self, request, *args, **kwargs):
        obj, _ = HeroSection.objects.get_or_create(pk=1)
        if not obj.photo_data:
            raise Http404("No hero photo set")

        etag = f'"{hashlib.sha256(bytes(obj.photo_data)).hexdigest()[:16]}"'
        if request.headers.get("If-None-Match") == etag:
            return HttpResponseNotModified()

        response = HttpResponse(bytes(obj.photo_data), content_type=obj.photo_content_type or "application/octet-stream")
        response["ETag"] = etag
        response["Cache-Control"] = "public, max-age=3600, stale-while-revalidate=86400"
        return response


class BrandSectionView(SingletonRetrieveAPIView):
    model = BrandSection
    serializer_class = BrandSectionSerializer


class ContactSectionView(SingletonRetrieveAPIView):
    model = ContactSection
    serializer_class = ContactSectionSerializer


class ExperienceSectionView(SingletonRetrieveAPIView):
    model = ExperienceSection
    serializer_class = ExperienceSectionSerializer


class ProjectsSectionView(SingletonRetrieveAPIView):
    model = ProjectsSection
    serializer_class = ProjectsSectionSerializer


class FunFactsSectionView(SingletonRetrieveAPIView):
    model = FunFactsSection
    serializer_class = FunFactsSectionSerializer


class TickerSectionView(SingletonRetrieveAPIView):
    model = TickerSection
    serializer_class = TickerSectionSerializer


class AboutSectionView(SingletonRetrieveAPIView):
    model = AboutSection
    serializer_class = AboutSectionSerializer


class StackSectionView(SingletonRetrieveAPIView):
    model = StackSection
    serializer_class = StackSectionSerializer
