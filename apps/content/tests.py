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


@pytest.mark.django_db
def test_hero_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/hero/")
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "eyebrow", "headline", "subheading", "photo", "cvUrl", "githubUrl", "linkedinUrl",
    }
    assert body["photo"] is None


@pytest.mark.django_db
def test_hero_section_reflects_saved_values(client):
    from apps.content.models import HeroSection

    HeroSection.objects.create(
        pk=1,
        eyebrow="Hi, I'm Jacob",
        headline="I build the systems behind the product",
        subheading="APIs, data pipelines, infrastructure.",
        cv_url="https://drive.google.com/x",
        github_url="https://github.com/jquaye",
        linkedin_url="https://linkedin.com/in/jquaye",
    )
    response = client.get("/api/content/hero/")
    body = response.json()
    assert body["headline"] == "I build the systems behind the product"
    assert body["cvUrl"] == "https://drive.google.com/x"
    assert body["githubUrl"] == "https://github.com/jquaye"
    assert body["linkedinUrl"] == "https://linkedin.com/in/jquaye"


@pytest.mark.django_db
def test_brand_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/brand/")
    assert response.status_code == 200
    assert response.json() == {"brands": []}


@pytest.mark.django_db
def test_brand_section_reflects_saved_values(client):
    from apps.content.models import BrandSection

    BrandSection.objects.create(pk=1, brands=["Acme", "Globex"])
    response = client.get("/api/content/brand/")
    assert response.json() == {"brands": ["Acme", "Globex"]}


@pytest.mark.django_db
def test_contact_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/contact/")
    assert response.status_code == 200
    assert response.json() == {"caption": "", "heading": "", "body": "", "email": "", "phone": ""}


@pytest.mark.django_db
def test_contact_section_reflects_saved_values(client):
    from apps.content.models import ContactSection

    ContactSection.objects.create(pk=1, caption="Get in touch", heading="Let's talk", body="Reach out.",
                                   email="jacob@example.com", phone="+1 555 0100")
    response = client.get("/api/content/contact/")
    body = response.json()
    assert body["email"] == "jacob@example.com"
    assert body["phone"] == "+1 555 0100"
