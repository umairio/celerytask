from rest_framework import serializers
from .models import User, Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


from rest_framework.permissions import IsAuthenticated


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


from datetime import timedelta, timezone


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def validate(self, data):
        if data["subscription_start_date"] > timezone.now() - timedelta(minutes=10):
            raise serializers.ValidationError("Subscription date cannot be older past")
        return data
