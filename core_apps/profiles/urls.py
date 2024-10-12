from django.urls import path
from .views import (
    AvatarUploadView,
    ProfileListAPIView,
    ProfileDetailAPIView,
    ProfileUpdateAPIView,
    NonTenantProfileListAPIView,
)

urlpatterns = [
    path("", ProfileListAPIView.as_view(), name="profile-list"),
    path(
        "non-tenant-profiles/",
        NonTenantProfileListAPIView.as_view(),
        name="non-tenant-profiles",
    ),
    path("user/me/", ProfileDetailAPIView.as_view(), name="profile-detail"),
    path("user/", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("user/avatar/", AvatarUploadView.as_view(), name="avatar-upload"),
]