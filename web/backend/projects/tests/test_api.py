import json

import pytest

pytest.importorskip("django", reason="Django web-backend dependencies are not installed")
pytest.importorskip("rest_framework", reason="Django REST Framework is required for API tests")

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from projects.models import BridgeProject, UserProfile

User = get_user_model()


class AccountAndProjectApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def register(self, username, email):
        return self.client.post(
            "/api/auth/register/",
            {"username": username, "email": email, "password": "S0lid-bridge-password!"},
            format="json",
        )

    def test_registration_hashes_password_and_opens_session(self):
        response = self.register("engineer", "engineer@example.test")
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="engineer")
        self.assertTrue(user.check_password("S0lid-bridge-password!"))
        self.assertEqual(UserProfile.objects.get(user=user).organization, "")
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 200)

    def test_registration_rejects_duplicate_username(self):
        self.register("engineer", "one@example.test")
        response = self.register("ENGINEER", "two@example.test")
        self.assertEqual(response.status_code, 400)

    def test_session_login_and_logout(self):
        User.objects.create_user(username="member", email="member@example.test", password="S0lid-bridge-password!")
        login_response = self.client.post(
            "/api/auth/login/",
            {"username": "member", "password": "S0lid-bridge-password!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 200)
        self.assertEqual(self.client.post("/api/auth/logout/").status_code, 204)

    def test_login_requires_csrf_token_when_checks_are_enabled(self):
        User.objects.create_user(username="csrf-user", password="S0lid-bridge-password!")
        client = APIClient(enforce_csrf_checks=True)
        missing = client.post(
            "/api/auth/login/",
            {"username": "csrf-user", "password": "S0lid-bridge-password!"},
            format="json",
        )
        self.assertEqual(missing.status_code, 403)
        csrf_response = client.get("/api/auth/csrf/")
        self.assertEqual(csrf_response.status_code, 200)
        token = csrf_response.data["csrfToken"]
        accepted = client.post(
            "/api/auth/login/",
            {"username": "csrf-user", "password": "S0lid-bridge-password!"},
            format="json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(accepted.status_code, 200)

    def test_profile_patch_persists_and_rejects_an_existing_email(self):
        self.register("profile-one", "one@example.test")
        changed = self.client.patch(
            "/api/auth/me/",
            {"organization": "Bridge office", "email": "updated@example.test"},
            format="json",
        )
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(changed.data["organization"], "Bridge office")
        self.register("profile-two", "two@example.test")
        duplicate = self.client.patch(
            "/api/auth/me/",
            {"email": "updated@example.test"},
            format="json",
        )
        self.assertEqual(duplicate.status_code, 400)

    def test_project_crud_is_limited_to_owner(self):
        self.register("owner", "owner@example.test")
        created = self.client.post(
            "/api/projects/",
            {
                "name": "North crossing",
                "bridge_type": "plate_girder",
                "location": "Example region",
                "configuration": {"geometry": {"span_m": 24.0}},
            },
            format="json",
        )
        self.assertEqual(created.status_code, 201)
        project_id = created.data["id"]
        self.assertEqual(BridgeProject.objects.get(pk=project_id).owner.username, "owner")
        self.assertEqual(self.client.patch(
            f"/api/projects/{project_id}/",
            {"description": "Updated project notes"},
            format="json",
        ).status_code, 200)

        self.client.post("/api/auth/logout/")
        self.register("other", "other@example.test")
        self.assertEqual(self.client.get("/api/projects/").data["count"], 0)
        self.assertEqual(self.client.get(f"/api/projects/{project_id}/").status_code, 404)
        self.assertEqual(self.client.delete(f"/api/projects/{project_id}/").status_code, 404)

    def test_geometry_validation_is_basic_input_validation_only(self):
        self.register("designer", "designer@example.test")
        good = self.client.post(
            "/api/geometry/validate/",
            {"bridge_type": "plate_girder", "geometry": {"span_m": 32.5, "width_m": 11.0}},
            format="json",
        )
        self.assertEqual(good.status_code, 200)
        self.assertIn("not an engineering adequacy", good.data["message"])
        bad = self.client.post(
            "/api/geometry/validate/",
            {"bridge_type": "plate_girder", "geometry": {"span_m": -1}},
            format="json",
        )
        self.assertEqual(bad.status_code, 400)

    def test_project_crud_rejects_nonpositive_geometry_inputs(self):
        self.register("geometry-user", "geometry@example.test")
        response = self.client.post(
            "/api/projects/",
            {
                "name": "Invalid input case",
                "bridge_type": "plate_girder",
                "configuration": {"geometry": {"span_m": 0}},
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(BridgeProject.objects.count(), 0)

    def test_json_export_contains_saved_inputs_not_analysis(self):
        self.register("exporter", "exporter@example.test")
        project = BridgeProject.objects.create(
            owner=User.objects.get(username="exporter"),
            name="Export case",
            configuration={"geometry": {"span_m": 18}},
        )
        response = self.client.get(f"/api/projects/{project.pk}/export/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("attachment;", response["Content-Disposition"])
        payload = json.loads(response.content)
        self.assertEqual(payload["configuration"]["geometry"]["span_m"], 18)
        self.assertNotIn("analysis_results", payload)

    def test_anonymous_users_cannot_list_projects(self):
        self.assertIn(self.client.get("/api/projects/").status_code, {401, 403})
