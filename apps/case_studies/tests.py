import pytest
from rest_framework.test import APIClient
from apps.case_studies.models import CaseStudy


@pytest.mark.django_db
def test_list_case_studies_empty(client):
    response = client.get("/api/case-studies/")
    assert response.status_code == 200
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_case_study_detail_shapes_response(client):
    CaseStudy.objects.create(
        slug="ledger",
        title="Ledger",
        date="2025-01-15",
        description="Double-entry accounting microservice.",
        tags=["Go", "PostgreSQL", "Redis"],
        source_url="https://github.com/example/ledger",
        featured=True,
        problem="p",
        architecture="a",
        my_role="r",
        outcome="o",
        banner="case_studies/ledger/banner.jpg",
    )
    response = client.get("/api/case-studies/ledger/")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Ledger"
    assert body["tags"] == ["Go", "PostgreSQL", "Redis"]
    assert body["sourceUrl"] == "https://github.com/example/ledger"
    assert body["myRole"] == "r"


@pytest.mark.django_db
def test_case_study_detail_404_for_unknown_slug(client):
    response = client.get("/api/case-studies/unknown-slug/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_unfeatured_case_study_hidden_from_public_list(client):
    CaseStudy.objects.create(
        slug="draft", title="Draft", date="2025-01-01", featured=False,
        banner="case_studies/draft/banner.jpg",
    )
    response = client.get("/api/case-studies/")
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_unfeatured_case_study_404s_on_public_detail(client):
    CaseStudy.objects.create(
        slug="draft", title="Draft", date="2025-01-01", featured=False,
        banner="case_studies/draft/banner.jpg",
    )
    response = client.get("/api/case-studies/draft/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_unfeatured_case_study_visible_to_staff(django_user_model):
    CaseStudy.objects.create(
        slug="draft", title="Draft", date="2025-01-01", featured=False,
        banner="case_studies/draft/banner.jpg",
    )
    staff = django_user_model.objects.create_user(username="admin", password="x", is_staff=True)
    # force_authenticate bypasses DRF's auth-class pipeline entirely (test
    # settings run with none configured), unlike a plain session login.
    api_client = APIClient()
    api_client.force_authenticate(user=staff)
    response = api_client.get("/api/case-studies/draft/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_case_study_write_requires_authentication(client):
    response = client.post("/api/case-studies/", {"title": "X", "date": "2025-01-01"})
    assert response.status_code in (401, 403)
