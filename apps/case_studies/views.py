from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CaseStudy
from .serializers import CaseStudyListSerializer, CaseStudyDetailSerializer, CaseStudyWriteSerializer
from .permissions import IsAdminOrReadOnly


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["date", "created_at", "title"]
    ordering = ["-date", "-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CaseStudyWriteSerializer
        if self.action == "retrieve":
            return CaseStudyDetailSerializer
        return CaseStudyListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # featured doubles as "published" — the public API only ever lists
        # featured case studies. Staff (admin) sees everything so they can
        # flip featured on before it goes live.
        user = self.request.user
        if not (user and user.is_authenticated and user.is_staff):
            queryset = queryset.filter(featured=True)
        return queryset