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
        if user.is_superuser or user.is_staff or (hasattr(user,profile) and user.profile.occupation == Profile.Occupation.TENANT):
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": _("Only superusers or staff members can create apartments.")}, status=status.HTTP_403_FORBIDDEN)


class ApartmentDetailsView(generics.ListAPIView):
    renderer_classes = (GenericJSONRenderer,)
    serializer_class = ApartmentSerializer
    object_label = "apartments"

    def get_queryset(self):
        return Apartment.objects.filter(tenant=self.request.user)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No apartments found for this user."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({'data': serializer.data})




