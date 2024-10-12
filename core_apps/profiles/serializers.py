from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from django_countries.serializer_fields import  CountryField
from core_apps.apartments.serializers import ApartmentSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")
    username = serializers.ReadOnlyField(source="user.username")
    full_name = serializers.ReadOnlyField(source="user.get_full_name")
    country_of_origin = CountryField(name_only=True)
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)
    apartments = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "slug",
            "first_name",
            "last_name",
            "username",
            "full_name",
            "gender",
            "country_of_origin",
            "city_of_origin",
            "bio",
            "occupation",
            "reputation",
            "date_joined",
            "avatar",
            "apartments",
            # "average_rating",
        ]

    def get_avatar(self, obj:Profile)-> str | None:
        try:
            return obj.avatar.url
        except AttributeError:
            return None

    def get_apartments(self, obj: Profile) -> list|None:
        apartments = obj.user.apartments.all()
        if apartments:
            return ApartmentSerializer(apartments, many=True).data
        return None

class UpdateProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")
    country_of_origin = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "username",
            "gender",
            "country_of_origin",
            "city_of_origin",
            "bio",
            "occupation",
            "phone_number",
        ]


class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["avatar"]
