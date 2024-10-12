from django.urls import path, re_path
from .views import ApartmentCreateAPIview, ApartmentDetailsView

urlpatterns = [
    path("", ApartmentCreateAPIview.as_view(), name="apartment-create"),
    path("me/", ApartmentDetailsView.as_view(), name="apartment-details")
]