from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    organization = models.CharField(max_length=180, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile for {self.user.get_username()}"


class BridgeProject(models.Model):
    class BridgeType(models.TextChoices):
        PLATE_GIRDER = "plate_girder", "Plate girder"
        BOX_GIRDER = "box_girder", "Box girder"
        TRUSS = "truss", "Truss"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bridge_projects")
    name = models.CharField(max_length=180)
    bridge_type = models.CharField(max_length=32, choices=BridgeType.choices, default=BridgeType.PLATE_GIRDER)
    location = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "name"]
        indexes = [models.Index(fields=["owner", "updated_at"], name="projects_owner_updated_idx")]

    def __str__(self) -> str:
        return self.name
