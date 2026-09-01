import time
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait for database to become available"

    def add_arguments(self, parser):
        parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds")
        parser.add_argument("--interval", type=int, default=2, help="Check interval in seconds")

    def handle(self, *args, **options):
        timeout = options["timeout"]
        interval = options["interval"]
        start = time.time()

        self.stdout.write("Waiting for database...")

        while time.time() - start < timeout:
            try:
                connection.ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError:
                self.stdout.write(f"Database unavailable, waiting {interval}s...")
                time.sleep(interval)

        self.stderr.write(self.style.ERROR(f"Database not available after {timeout}s"))
        raise SystemExit(1)