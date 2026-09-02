import re
from datetime import date, datetime

import django.db.models.deletion
from django.db import migrations, models


def parse_period(period_str):
    """Best-effort parse of the old free-text period strings this data
    migration is converting away from, e.g. 'Nov 2025 — Present' or
    '2023 — Nov 2025'. Accepts a bare year or 'Mon YYYY' on either side."""
    period_str = (period_str or "").strip()
    parts = [p.strip() for p in re.split(r"—|-", period_str, maxsplit=1)]
    start_str = parts[0] if parts else ""
    end_str = parts[1] if len(parts) > 1 else "Present"

    def parse_one(s):
        s = s.strip()
        if re.fullmatch(r"\d{4}", s):
            return date(int(s), 1, 1)
        try:
            return datetime.strptime(s, "%b %Y").date()
        except ValueError:
            return None

    start = parse_one(start_str) or date.today()
    end = None if end_str.lower() == "present" else parse_one(end_str)
    return start, end


def migrate_experiences_to_rows(apps, schema_editor):
    ExperienceSection = apps.get_model("content", "ExperienceSection")
    Experience = apps.get_model("content", "Experience")
    for section in ExperienceSection.objects.all():
        for index, item in enumerate(section.experiences or []):
            start, end = parse_period(item.get("period", ""))
            Experience.objects.create(
                section=section,
                role=item.get("role", ""),
                company=item.get("company", ""),
                start_date=start,
                end_date=end,
                order=index,
            )


def delete_experience_rows(apps, schema_editor):
    # Best-effort reverse: drops the rows. Doesn't attempt to reconstruct
    # the original free-text period strings byte-for-byte.
    Experience = apps.get_model("content", "Experience")
    Experience.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0011_seed_real_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="Experience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(max_length=200)),
                ("company", models.CharField(max_length=200)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        # Temporary name — the old JSONField below is still
                        # called "experiences" at this point in the
                        # migration's model state, so the reverse accessor
                        # can't claim that name yet without colliding.
                        # Renamed to "experiences" once that field is gone.
                        related_name="experience_rows_tmp",
                        to="content.experiencesection",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "-start_date"],
            },
        ),
        migrations.RunPython(migrate_experiences_to_rows, delete_experience_rows),
        migrations.RemoveField(
            model_name="experiencesection",
            name="experiences",
        ),
        migrations.AlterField(
            model_name="experience",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiences",
                to="content.experiencesection",
            ),
        ),
    ]
