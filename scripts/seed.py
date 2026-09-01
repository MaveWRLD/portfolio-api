#!/usr/bin/env python
"""
Seed script to populate the database with initial case studies.
Run: python scripts/seed.py
"""
import os
import sys
import django
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.core.files.base import ContentFile
from apps.case_studies.models import CaseStudy

CASE_STUDIES = [
    {
        "slug": "portfolio-api",
        "category": "Backend",
        "date": "2025-01-15",
        "title": "Portfolio API",
        "detail_title": "Django REST API for Portfolio Case Studies",
        "budget": "Personal Project",
        "client": "Self",
        "tool": "Django, DRF, PostgreSQL, JWT, S3",
        "featured": True,
        "banner": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800",
        "gallery": [
            {"src": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800", "aspect": 1.778},
            {"src": "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600", "aspect": 0.867},
            {"src": "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600", "aspect": 0.867},
        ],
    },
    {
        "slug": "distributed-task-queue",
        "category": "Systems",
        "date": "2024-11-20",
        "title": "Distributed Task Queue",
        "detail_title": "Redis-backed Task Queue with Retry Logic",
        "budget": "Open Source",
        "client": "GitHub Community",
        "tool": "Python, Redis, Celery, Docker",
        "featured": False,
        "banner": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800",
        "gallery": [
            {"src": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800", "aspect": 1.778},
            {"src": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600", "aspect": 0.867},
            {"src": "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600", "aspect": 0.867},
        ],
    },
    {
        "slug": "api-gateway",
        "category": "Infrastructure",
        "date": "2024-09-10",
        "title": "API Gateway Service",
        "detail_title": "High-throughput Gateway with Rate Limiting",
        "budget": "Contract",
        "client": "Fintech Startup",
        "tool": "Go, Kong, PostgreSQL, Prometheus",
        "featured": True,
        "banner": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
        "gallery": [
            {"src": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800", "aspect": 1.778},
            {"src": "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600", "aspect": 0.867},
            {"src": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600", "aspect": 0.867},
        ],
    },
    {
        "slug": "data-pipeline",
        "category": "Data",
        "date": "2024-06-05",
        "title": "ETL Data Pipeline",
        "detail_title": "Real-time Analytics Pipeline",
        "budget": "Internal Tool",
        "client": "E-commerce Platform",
        "tool": "Python, Airflow, ClickHouse, Kafka",
        "featured": False,
        "banner": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
        "gallery": [
            {"src": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800", "aspect": 1.778},
            {"src": "https://images.unsplash.com/photo-1518432031352-d6fc5c10da5a?w=600", "aspect": 0.867},
            {"src": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=600", "aspect": 0.867},
        ],
    },
]


def seed():
    created = 0
    updated = 0

    for data in CASE_STUDIES:
        obj, is_created = CaseStudy.objects.update_or_create(
            slug=data["slug"],
            defaults=data,
        )
        if is_created:
            created += 1
            print(f"Created: {obj.title}")
        else:
            updated += 1
            print(f"Updated: {obj.title}")

    print(f"\nDone. Created: {created}, Updated: {updated}")


if __name__ == "__main__":
    seed()