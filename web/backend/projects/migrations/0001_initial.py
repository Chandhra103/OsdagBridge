# Initial schema for user profiles and persisted bridge project inputs.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("organization", models.CharField(blank=True, max_length=180)),
                ("job_title", models.CharField(blank=True, max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BridgeProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=180)),
                (
                    "bridge_type",
                    models.CharField(
                        choices=[
                            ("plate_girder", "Plate girder"),
                            ("box_girder", "Box girder"),
                            ("truss", "Truss"),
                        ],
                        default="plate_girder",
                        max_length=32,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=180)),
                ("description", models.TextField(blank=True)),
                ("configuration", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bridge_projects",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at", "name"],
                "indexes": [models.Index(fields=["owner", "updated_at"], name="projects_owner_updated_idx")],
            },
        ),
    ]
