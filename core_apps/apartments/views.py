from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from typing import Any

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from core_apps.profiles.models import Profile
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from .serializers import ApartmentSerializer, UpdateApartmentSerializer
from django.utils.translation import gettext_lazy as _
from .models import Apartment
from rest_framework.response import Response
from rest_framework.request import Request
from core_apps.common.renderers import GenericJSONRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny  # More concise
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

User = get_user_model()
# import  logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

class ApartmentListAPIView(generics.ListAPIView):
    renderer_classes = (GenericJSONRenderer,)
    serializer_class = ApartmentSerializer
    permission_classes = (AllowAny,)
    object_label = "apartments"

    def get_queryset(self):
        return Apartment.objects.filter(tenant=None)


class ApartmentCreateAPIview(generics.CreateAPIView):
    renderer_classes = (GenericJSONRenderer,)
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    object_label = "apartment"

    def create(self, request: Request, *args: Any, **kwargs: Any):
        user = request.user
        if user.is_superuser or user.is_staff or (
                hasattr(user, "profile") and user.profile.occupation == Profile.Occupation.TENANT):
            return super().create(request, *args, **kwargs)
        else:
            return Response({"message": _("Only superusers or staff members can create apartments.")},
                            status=status.HTTP_403_FORBIDDEN)


class ApartmentDetailsView(generics.ListAPIView):
    renderer_classes = (GenericJSONRenderer,)
    serializer_class = ApartmentSerializer
    object_label = "apartments"

    def get_queryset(self):
        return Apartment.objects.filter(tenant=self.request.user)

class ApartmentReleaseView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Libérer un appartement",
        operation_description="Permet à un administrateur ou au locataire actuel de libérer (désassigner) un appartement.",
        manual_parameters=[
            openapi.Parameter(
                'apartment_id',
                openapi.IN_PATH,
                description="ID de l'appartement à libérer",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Appartement libéré avec succès",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message de confirmation",
                            example="Apartment successfully released."
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="L'appartement n'est pas actuellement loué",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message d'erreur",
                            example="Apartment is not currently rented."
                        )
                    }
                )
            ),
            403: openapi.Response(
                description="Permission refusée",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message d'erreur de permission",
                            example="Only admin members or the apartment tenant can release apartments."
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Appartement non trouvé",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message d'erreur de non-existence",
                            example="Apartment not found."
                        )
                    }
                )
            )
        }
    )

    def patch(self, request, *args, **kwargs):
        apartment_id = kwargs.get('apartment_id')

        try:
            # Fetch the apartment with its related tenant
            apartment = Apartment.objects.select_related('tenant').get(id=apartment_id)

            # Check if the apartment is actually rented
            if apartment.tenant is None:
                return Response(
                    {"message": "Apartment is not currently rented."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Check user permissions
            if not (request.user.is_superuser or
                    request.user.is_staff or
                    request.user == apartment.tenant):
                raise PermissionDenied(
                    "Only admin members or the apartment tenant can release apartments."
                )
            # Release the apartment
            apartment.tenant = None
            apartment.save()

            return Response(
                {"message": "Apartment successfully released."},
                status=status.HTTP_200_OK
            )

        except Apartment.DoesNotExist:
            return Response(
                {"message": "Apartment not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class ApartmentAssignView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = UpdateApartmentSerializer
    # object_label = "Apartment"
    # renderer_classes = ( GenericJSONRenderer, )

    @swagger_auto_schema(
        operation_summary="Attribuer un appartement à un locataire",
        operation_description="Permet à un administrateur d'attribuer un appartement disponible à un locataire.",
        manual_parameters=[
            openapi.Parameter(
                'apartment_id',
                openapi.IN_PATH,
                description="ID de l'appartement à attribuer",
                type=openapi.TYPE_INTEGER
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['tenant'],
            properties={
                'tenant': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID du locataire à qui attribuer l'appartement",
                    example="5e2e7a29-0c72-432d-be62-a108c77e9900"

                )
            }
        ),
        responses={
            200: openapi.Response(
                description="Appartement attribué avec succès",
                schema= UpdateApartmentSerializer
            ),
            400: openapi.Response(
                description="Locataire invalide ou appartement déjà attribué",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message d'erreur",
                            enum=["User must be a tenant.", "Apartment is already assigned."]
                        )
                    }
                )
            ),
            404: openapi.Response(
                description="Locataire ou appartement non trouvé",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Message d'erreur de non-existence",
                            enum=["Tenant not found.", "Apartment not found."]
                        )
                    }
                )
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        # Validate tenant
        tenant_id = request.data.get('tenant')
        try:
            tenant = User.objects.select_related('profile').get(id=tenant_id)

            # Ensure tenant has correct occupation
            if not hasattr(tenant, 'profile') or tenant.profile.occupation != Profile.Occupation.TENANT:
                return Response(
                    {"message": "User must be a tenant."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except User.DoesNotExist:
            return Response(
                {"message": "Tenant not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate apartment
        apartment_id = kwargs.get("apartment_id")
        try:
            apartment = Apartment.objects.select_related("tenant").get(id=apartment_id)

            # Check apartment availability
            if apartment.tenant is not None:
                return Response(
                    {"message": "Apartment is already assigned."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Assign apartment
            apartment.tenant = tenant
            apartment.save()

            # Serialize the updated apartment
            serializer = self.serializer_class(apartment)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        except Apartment.DoesNotExist:
            return Response(
                {"message": "Apartment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

