import pytest


@pytest.mark.django_db
def test_site_settings_get_creates_singleton_and_shapes_response(client):
    # A data migration (0011_seed_real_content) pre-populates pk=1 with real
    # content, so this checks shape, not blank values.
    response = client.get("/api/content/settings/")
    assert response.status_code == 200
    assert set(response.json().keys()) == {"name", "footerTagline"}


@pytest.mark.django_db
def test_site_settings_reflects_saved_values(client):
    from apps.content.models import SiteSettings

    SiteSettings.objects.update_or_create(
        pk=1, defaults={"name": "Jacob Quaye", "footer_tagline": "Backend engineer"}
    )
    response = client.get("/api/content/settings/")
    assert response.json() == {"name": "Jacob Quaye", "footerTagline": "Backend engineer"}


@pytest.mark.django_db
def test_hero_section_get_creates_singleton_and_shapes_response(client):
    # Seeded by 0015_seed_local_snapshot (photo included) — checks shape,
    # not blank values.
    response = client.get("/api/content/hero/")
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {
        "eyebrow", "headline", "subheading", "photo", "cvUrl", "githubUrl", "linkedinUrl",
    }
    assert body["photo"].startswith("http://testserver/api/content/hero/photo/")


@pytest.mark.django_db
def test_hero_section_reflects_saved_values(client):
    from apps.content.models import HeroSection

    HeroSection.objects.update_or_create(
        pk=1,
        defaults={
            "eyebrow": "Hi, I'm Jacob",
            "headline": "I build the systems behind the product",
            "subheading": "APIs, data pipelines, infrastructure.",
            "cv_url": "https://drive.google.com/x",
            "github_url": "https://github.com/jquaye",
            "linkedin_url": "https://linkedin.com/in/jquaye",
        },
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
    # Seeded by 0015_seed_local_snapshot — checks shape, not blank values.
    response = client.get("/api/content/contact/")
    assert response.status_code == 200
    assert set(response.json().keys()) == {"caption", "heading", "body", "email", "phone"}


@pytest.mark.django_db
def test_contact_section_reflects_saved_values(client):
    from apps.content.models import ContactSection

    ContactSection.objects.update_or_create(
        pk=1,
        defaults=dict(caption="Get in touch", heading="Let's talk", body="Reach out.",
                      email="jacob@example.com", phone="+1 555 0100"),
    )
    response = client.get("/api/content/contact/")
    body = response.json()
    assert body["email"] == "jacob@example.com"
    assert body["phone"] == "+1 555 0100"


@pytest.mark.django_db
def test_experience_section_get_creates_singleton_and_shapes_response(client):
    # Seeded by 0011_seed_real_content — checks shape, not blank values.
    response = client.get("/api/content/experience/")
    assert response.status_code == 200
    assert set(response.json().keys()) == {"heading", "body", "experiences"}


@pytest.mark.django_db
def test_experience_section_reflects_saved_values(client):
    from apps.content.models import ExperienceSection, Experience

    section, _ = ExperienceSection.objects.update_or_create(
        pk=1, defaults={"heading": "Experience", "body": "Where I've worked."}
    )
    section.experiences.all().delete()
    Experience.objects.create(
        section=section, company="Acme", role="Backend Engineer",
        start_date="2022-01-01", end_date=None, order=0,
    )
    response = client.get("/api/content/experience/")
    body = response.json()
    assert body["experiences"] == [{"company": "Acme", "role": "Backend Engineer", "period": "Jan 2022 — Present"}]


@pytest.mark.django_db
def test_projects_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/projects/")
    assert response.status_code == 200
    assert response.json() == {"heading": ""}


@pytest.mark.django_db
def test_projects_section_reflects_saved_values(client):
    from apps.content.models import ProjectsSection

    ProjectsSection.objects.create(pk=1, heading="Selected work")
    response = client.get("/api/content/projects/")
    assert response.json() == {"heading": "Selected work"}


@pytest.mark.django_db
def test_fun_facts_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/fun-facts/")
    assert response.status_code == 200
    assert response.json() == {"heading": "", "stats": [], "testimonials": []}


@pytest.mark.django_db
def test_fun_facts_section_reflects_saved_values(client):
    from apps.content.models import FunFactsSection

    FunFactsSection.objects.create(
        pk=1, heading="By the numbers",
        stats=[{"value": "10+", "label": "Years"}],
        testimonials=[{"category": "Client", "quote": "Great work.", "author": "Jane Doe", "authorRole": "CTO"}],
    )
    response = client.get("/api/content/fun-facts/")
    body = response.json()
    assert body["stats"] == [{"value": "10+", "label": "Years"}]
    assert body["testimonials"][0]["authorRole"] == "CTO"


@pytest.mark.django_db
def test_ticker_section_get_creates_singleton_and_shapes_response(client):
    response = client.get("/api/content/ticker/")
    assert response.status_code == 200
    assert response.json() == {"phrases": []}


@pytest.mark.django_db
def test_ticker_section_reflects_saved_values(client):
    from apps.content.models import TickerSection

    TickerSection.objects.create(pk=1, phrases=["Available for hire", "Based in Accra"])
    response = client.get("/api/content/ticker/")
    assert response.json() == {"phrases": ["Available for hire", "Based in Accra"]}


@pytest.mark.django_db
def test_about_section_get_creates_singleton_and_shapes_response(client):
    # Seeded by 0011_seed_real_content — checks shape, not blank values.
    response = client.get("/api/content/about/")
    assert response.status_code == 200
    assert set(response.json().keys()) == {"heading", "body"}


@pytest.mark.django_db
def test_about_section_reflects_saved_values(client):
    from apps.content.models import AboutSection

    AboutSection.objects.update_or_create(pk=1, defaults={"heading": "About", "body": "I build backend systems."})
    response = client.get("/api/content/about/")
    assert response.json() == {"heading": "About", "body": "I build backend systems."}


@pytest.mark.django_db
def test_stack_section_get_creates_singleton_and_shapes_response(client):
    # Seeded by 0011_seed_real_content — checks shape, not blank values.
    response = client.get("/api/content/stack/")
    assert response.status_code == 200
    assert set(response.json().keys()) == {"languages", "data", "infra"}


@pytest.mark.django_db
def test_stack_section_reflects_saved_values(client):
    from apps.content.models import StackSection, Technology

    section, _ = StackSection.objects.get_or_create(pk=1)
    section.technologies.all().delete()
    Technology.objects.create(section=section, name="Go", category="language", order=0)
    Technology.objects.create(section=section, name="Python", category="language", order=1)
    Technology.objects.create(section=section, name="PostgreSQL", category="data", order=0)
    Technology.objects.create(section=section, name="Docker", category="infra", order=0)
    Technology.objects.create(section=section, name="AWS", category="infra", order=1)

    response = client.get("/api/content/stack/")
    body = response.json()
    assert body["languages"] == ["Go", "Python"]
    assert body["infra"] == ["Docker", "AWS"]
