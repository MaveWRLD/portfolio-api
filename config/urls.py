from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from apps.case_studies.views import CaseStudyViewSet
from apps.content.views import (
    SiteSettingsView, HeroSectionView, HeroPhotoView, BrandSectionView, ContactSectionView,
    ExperienceSectionView, ProjectsSectionView, FunFactsSectionView, TickerSectionView, AboutSectionView,
    StackSectionView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"case-studies", CaseStudyViewSet, basename="case-study")

urlpatterns = [
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/content/settings/", SiteSettingsView.as_view(), name="content-settings"),
    path("api/content/hero/", HeroSectionView.as_view(), name="content-hero"),
    path("api/content/hero/photo/", HeroPhotoView.as_view(), name="content-hero-photo"),
    path("api/content/brand/", BrandSectionView.as_view(), name="content-brand"),
    path("api/content/contact/", ContactSectionView.as_view(), name="content-contact"),
    path("api/content/experience/", ExperienceSectionView.as_view(), name="content-experience"),
    path("api/content/projects/", ProjectsSectionView.as_view(), name="content-projects"),
    path("api/content/fun-facts/", FunFactsSectionView.as_view(), name="content-fun-facts"),
    path("api/content/ticker/", TickerSectionView.as_view(), name="content-ticker"),
    path("api/content/about/", AboutSectionView.as_view(), name="content-about"),
    path("api/content/stack/", StackSectionView.as_view(), name="content-stack"),
    path("api/health/", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if "silk" in settings.INSTALLED_APPS:
    urlpatterns = [path("silk/", include("silk.urls", namespace="silk"))] + urlpatterns
