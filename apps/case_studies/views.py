from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import CaseStudy
from .serializers import CaseStudyListSerializer, CaseStudyDetailSerializer, CaseStudyWriteSerializer
from .permissions import IsAdminOrReadOnly


class CaseStudyViewSet(viewsets.ModelViewSet):
    queryset = CaseStudy.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["featured"]
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
        featured = self.request.query_params.get("featured")
        if featured is not None:
            queryset = queryset.filter(featured=featured.lower() == "true")
        return queryset