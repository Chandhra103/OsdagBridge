import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from projects.api.serializers import (
    BridgeProjectSerializer,
    GeometryValidationSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
)
from projects.models import BridgeProject, UserProfile


@ensure_csrf_cookie
@api_view(["GET"])
@permission_classes([AllowAny])
def csrf_token(request):
    return Response({"csrfToken": get_token(request)})


@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    login(request, user)
    profile = UserProfile.objects.get(user=user)
    return Response(UserProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def session_login(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    if not isinstance(username, str) or not isinstance(password, str) or not username or not password:
        return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "The supplied credentials are invalid."}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return Response(UserProfileSerializer(profile).data)


@csrf_protect
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def session_logout(request):
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def current_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "GET":
        return Response(UserProfileSerializer(profile).data)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


class BridgeProjectViewSet(viewsets.ModelViewSet):
    serializer_class = BridgeProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BridgeProject.objects.filter(owner=self.request.user).select_related("owner")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def export(self, request, *args, **kwargs):
        project = self.get_object()
        payload = BridgeProjectSerializer(project).data
        response = HttpResponse(
            json.dumps(payload, indent=2, ensure_ascii=False),
            content_type="application/json; charset=utf-8",
        )
        response["Content-Disposition"] = f'attachment; filename="osdagbridge-project-{project.pk}.json"'
        return response


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def validate_geometry(request):
    serializer = GeometryValidationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({
        "valid": True,
        "scope": "basic input validation only",
        "message": "Inputs are syntactically valid; this is not an engineering adequacy check.",
    })
