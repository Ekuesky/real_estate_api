from rest_framework import generics, status
from .serializers import ApartmentSerializer
from django.utils.translation import gettext_lazy as _
from .models import  Apartment
from rest_framework.response import Response
from rest_framework.request import Request
from core_apps.common.renderers import GenericJSONRenderer
from typing import Any, List
from core_apps.profiles.models import Profile

class ApartmentCreateAPIview(generics.CreateAPIView):
    renderer_classes = (GenericJSONRenderer,)
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    object_label = "apartment"

    def create(self, request:Request, *args:Any, **kwargs:Any):
        user = request.user
        if user.is_superuser or (hasattr(user,profile) and user.profile.occupation == Profile.Occupation.TENANT):
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": _("Only tenants, superusers or staff members can create apartments.")}, status=status.HTTP_403_FORBIDDEN)


class ApartmentDetailsView(generics.RetrieveAPIView):
    renderer_classes = (GenericJSONRenderer,)
    serializer_class = ApartmentSerializer
    object_label = "apartment"

    def get_object(self)->Apartment:
        query = self.request.user.apartment.all()
        if query:
            obj = generics.get_object_or_404(query)
            return obj



