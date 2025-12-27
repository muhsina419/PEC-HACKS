from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "password",
            "first_name",
            "last_name",
            "email",
            "city",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "city",
            "avatar_url",
            "eco_score",
        ]
        read_only_fields = ["phone_number", "eco_score"]


class PhoneTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "phone_number"

    def validate(self, attrs):
        attrs[self.username_field] = attrs.get("phone_number")
        return super().validate(attrs)
