from django.urls import path, re_path
from .views import ApartmentCreateAPIview, ApartmentDetailsView, ApartmentListAPIView, ApartmentReleaseView, \
    ApartmentAssignView

urlpatterns = [
    path("", ApartmentCreateAPIview.as_view(), name="apartment-create"),
    path("me/", ApartmentDetailsView.as_view(), name="apartment-details"),
    path("available/", ApartmentListAPIView.as_view(), name="apartment-non-assigned"),
    path('<uuid:apartment_id>/release/', ApartmentReleaseView.as_view(), name='apartment-release'),
    path('<uuid:apartment_id>/assign/', ApartmentAssignView.as_view(), name='apartment-assign'),
]