from django.urls import path, re_path
from .views import ApartmentCreateAPIview, ApartmentDetailsView

urlpatterns = [
    path("add/", ApartmentCreateAPIview.as_view(), name="apartment-create"),
    path("me-aparts/", ApartmentDetailsView.as_view(), name="apartment-details")
]