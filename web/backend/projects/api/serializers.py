import math

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from projects.models import BridgeProject, UserProfile

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False, min_length=8)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("An account with this username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = ["username", "email", "first_name", "last_name", "organization", "job_title"]

    def validate_email(self, value):
        users = User.objects.filter(email__iexact=value)
        if self.instance is not None:
            users = users.exclude(pk=self.instance.user_id)
        if users.exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for field, value in user_data.items():
            setattr(instance.user, field, value)
        if user_data:
            instance.user.save()
        return super().update(instance, validated_data)


class BridgeProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = BridgeProject
        fields = [
            "id", "name", "bridge_type", "location", "description", "configuration",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_configuration(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Configuration must be a JSON object.")
        geometry = value.get("geometry")
        if geometry is not None:
            bridge_type = self.initial_data.get("bridge_type")
            if bridge_type is None and self.instance is not None:
                bridge_type = self.instance.bridge_type
            if bridge_type is None:
                bridge_type = BridgeProject.BridgeType.PLATE_GIRDER
            check = GeometryValidationSerializer(
                data={"bridge_type": bridge_type, "geometry": geometry}
            )
            if not check.is_valid():
                raise serializers.ValidationError(check.errors)
        return value


class GeometryValidationSerializer(serializers.Serializer):
    bridge_type = serializers.ChoiceField(choices=BridgeProject.BridgeType.choices)
    geometry = serializers.DictField()

    def validate_geometry(self, value):
        for field in ("span_m", "width_m"):
            if field not in value:
                continue
            try:
                number = float(value[field])
            except (TypeError, ValueError):
                raise serializers.ValidationError({field: "Must be a finite positive number in metres."})
            if not math.isfinite(number) or number <= 0:
                raise serializers.ValidationError({field: "Must be a finite positive number in metres."})
        return value
