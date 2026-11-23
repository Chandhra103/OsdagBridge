from django.urls import include, path
from rest_framework.routers import DefaultRouter

from projects.api.views import (
    BridgeProjectViewSet,
    csrf_token,
    current_profile,
    register,
    session_login,
    session_logout,
    validate_geometry,
)

router = DefaultRouter()
router.register("projects", BridgeProjectViewSet, basename="project")

urlpatterns = [
    path("auth/csrf/", csrf_token, name="csrf-token"),
    path("auth/register/", register, name="register"),
    path("auth/login/", session_login, name="login"),
    path("auth/logout/", session_logout, name="logout"),
    path("auth/me/", current_profile, name="profile"),
    path("geometry/validate/", validate_geometry, name="validate-geometry"),
    path("", include(router.urls)),
]

# Project-input JSON export returns saved data only, not an engineering report.
urlpatterns += [
    path(
        "projects/<int:pk>/export/",
        BridgeProjectViewSet.as_view({"get": "export"}),
        name="project-export",
    ),
]
