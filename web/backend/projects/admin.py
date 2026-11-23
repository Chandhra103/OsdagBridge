from django.contrib import admin

from projects.models import BridgeProject, UserProfile


@admin.register(BridgeProject)
class BridgeProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "bridge_type", "owner", "updated_at")
    list_filter = ("bridge_type", "updated_at")
    search_fields = ("name", "owner__username", "location")
    readonly_fields = ("created_at", "updated_at")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "job_title", "updated_at")
    search_fields = ("user__username", "user__email", "organization")
