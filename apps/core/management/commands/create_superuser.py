import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser non-interactively from env vars (safe to run every deploy)"

    def add_arguments(self, parser):
        parser.add_argument("--username", default=os.getenv("DJANGO_SUPERUSER_USERNAME", "admin"))
        parser.add_argument("--email", default=os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com"))
        parser.add_argument("--password", default=os.getenv("DJANGO_SUPERUSER_PASSWORD"))

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if not password:
            self.stdout.write("DJANGO_SUPERUSER_PASSWORD not set, skipping superuser creation")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User '{username}' already exists, skipping")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
