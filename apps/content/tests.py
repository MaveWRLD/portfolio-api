import pytest


@pytest.mark.django_db
def test_site_settings_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/settings/")
    assert response.status_code == 200
    assert response.json() == {"name": "", "footerTagline": ""}


@pytest.mark.django_db
def test_site_settings_reflects_saved_values(client):
    from apps.content.models import SiteSettings

    SiteSettings.objects.create(pk=1, name="Jacob Quaye", footer_tagline="Backend engineer")
    response = client.get("/api/content/settings/")
    assert response.json() == {"name": "Jacob Quaye", "footerTagline": "Backend engineer"}
