import uuid

from rest_framework import serializers
from .models import Apartment



class ApartmentSerializer(serializers.ModelSerializer):
    #tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tenant = serializers.HiddenField(default=None)
    class Meta:
        model = Apartment
        exclude = ["pkid", "updated_at",]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request')
    #     if request and request.user == instance.tenant:
    #         # Si l'utilisateur actuel est le locataire, nous incluons toutes les informations
    #         return representation
    #     else:
    #         # Sinon, nous excluons certaines informations sensibles
    #         sensitive_fields = ['tenant']  # Ajoutez d'autres champs sensibles si nécessaire
    #         for field in sensitive_fields:
    #             representation.pop(field, None)
    #     return representation

class UpdateApartmentSerializer(serializers.ModelSerializer):

    tenant = serializers.UUIDField(default=uuid.uuid4, required=False,allow_null= False)
    class Meta:
        model = Apartment
        fields = ["unit_number", "building", "floor","tenant"]
        read_only_fields = ["unit_number", "building", "floor" ]




