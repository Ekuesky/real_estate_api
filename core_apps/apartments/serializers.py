from rest_framework import serializers
from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    # Le champ 'tenant' est caché, ne sera pas inclus dans la réponse JSON
    # et sera automatiquement rempli par le champ 'current_user' de Django REST Framework.
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Apartment
        exclude = ["pkid", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user == instance.tenant:
            # Si l'utilisateur actuel est le locataire, nous incluons toutes les informations
            return representation
        else:
            # Sinon, nous excluons certaines informations sensibles
            sensitive_fields = ['tenant']  # Ajoutez d'autres champs sensibles si nécessaire
            for field in sensitive_fields:
                representation.pop(field, None)
        return representation