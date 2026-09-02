import django.db.models.deletion
from django.db import migrations, models


def migrate_arrays_to_rows(apps, schema_editor):
    StackSection = apps.get_model("content", "StackSection")
    Technology = apps.get_model("content", "Technology")
    for section in StackSection.objects.all():
        for category, names in (
            ("language", section.languages or []),
            ("data", section.data or []),
            ("infra", section.infra or []),
        ):
            for index, name in enumerate(names):
                Technology.objects.create(section=section, name=name, category=category, order=index)


def delete_technology_rows(apps, schema_editor):
    Technology = apps.get_model("content", "Technology")
    Technology.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0012_experience_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="Technology",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[("language", "Language"), ("data", "Data"), ("infra", "Infra")],
                        max_length=20,
                    ),
                ),
                ("icon", models.CharField(blank=True, default="", max_length=100)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="technologies",
                        to="content.stacksection",
                    ),
                ),
            ],
            options={
                "ordering": ["category", "order", "name"],
            },
        ),
        migrations.RunPython(migrate_arrays_to_rows, delete_technology_rows),
        migrations.RemoveField(model_name="stacksection", name="languages"),
        migrations.RemoveField(model_name="stacksection", name="data"),
        migrations.RemoveField(model_name="stacksection", name="infra"),
    ]
