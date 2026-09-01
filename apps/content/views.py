from rest_framework import generics
from .models import SiteSettings, HeroSection, BrandSection, ContactSection
from .serializers import (
    SiteSettingsSerializer, HeroSectionSerializer, BrandSectionSerializer, ContactSectionSerializer,
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


class BrandSectionView(SingletonRetrieveAPIView):
    model = BrandSection
    serializer_class = BrandSectionSerializer


class ContactSectionView(SingletonRetrieveAPIView):
    model = ContactSection
    serializer_class = ContactSectionSerializer
