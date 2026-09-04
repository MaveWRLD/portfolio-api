from django.db import migrations

SITE_SETTINGS = {
    "name": "Jacob Quaye",
    "footer_tagline": "Backend Engineer",
}

HERO = {
    "eyebrow": "Backend Engineer",
    "headline": "I build reliable backend systems that scale",
    "subheading": (
        "APIs, microservices, and data pipelines built with Java/Spring Boot and Django — "
        "from ticketing engines to real-time inventory systems."
    ),
    "github_url": "https://github.com/mavewrld",
    "linkedin_url": "https://linkedin.com/in/jacobquaye",
}

ABOUT = {
    "heading": "About",
    "body": (
        "I'm a backend engineer based in Kumasi, Ghana, building scalable web applications "
        "and APIs in fast-paced product environments. My focus is reliable, well-tested "
        "software — from Java/Spring Boot services to Django REST APIs — with a practical, "
        "quality-first approach shaped by hands-on work across development, testing, and "
        "release cycles."
    ),
}

STACK = {
    "languages": ["Java", "Spring Boot", "Django REST Framework", "REST APIs"],
    "data": ["PostgreSQL", "MongoDB", "Redis", "Kafka"],
    "infra": ["Docker", "AWS", "Git", "Jenkins/CI-CD"],
}

EXPERIENCE = {
    "heading": "Experience",
    "body": "Where I've worked.",
    "experiences": [
        {"company": "Amalitech", "role": "Backend Engineer", "period": "Nov 2025 — Present"},
        {"company": "Self-Employed", "role": "Freelance Software Developer", "period": "2023 — Nov 2025"},
    ],
}


def seed_content(apps, schema_editor):
    SiteSettings = apps.get_model("content", "SiteSettings")
    HeroSection = apps.get_model("content", "HeroSection")
    AboutSection = apps.get_model("content", "AboutSection")
    StackSection = apps.get_model("content", "StackSection")
    ExperienceSection = apps.get_model("content", "ExperienceSection")

    SiteSettings.objects.update_or_create(pk=1, defaults=SITE_SETTINGS)
    HeroSection.objects.update_or_create(pk=1, defaults=HERO)
    AboutSection.objects.update_or_create(pk=1, defaults=ABOUT)
    StackSection.objects.update_or_create(pk=1, defaults=STACK)
    ExperienceSection.objects.update_or_create(pk=1, defaults=EXPERIENCE)


def unseed_content(apps, schema_editor):
    # Reversal clears the seeded rows back to blank rather than deleting them —
    # the singleton pattern expects pk=1 to always exist.
    SiteSettings = apps.get_model("content", "SiteSettings")
    HeroSection = apps.get_model("content", "HeroSection")
    AboutSection = apps.get_model("content", "AboutSection")
    StackSection = apps.get_model("content", "StackSection")
    ExperienceSection = apps.get_model("content", "ExperienceSection")

    SiteSettings.objects.filter(pk=1).update(name="", footer_tagline="")
    HeroSection.objects.filter(pk=1).update(
        eyebrow="", headline="", subheading="", github_url="", linkedin_url="",
    )
    AboutSection.objects.filter(pk=1).update(heading="", body="")
    StackSection.objects.filter(pk=1).update(languages=[], data=[], infra=[])
    ExperienceSection.objects.filter(pk=1).update(heading="", body="", experiences=[])


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0010_stacksection"),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
