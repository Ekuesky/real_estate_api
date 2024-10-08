from rest_framework import serializers
from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    # Le champ 'tenant' est caché, ne sera pas inclus dans la réponse JSON
    # et sera automatiquement rempli par le champ 'current_user' de Django REST Framework.
    tenant = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Apartment
        exclude = ["pkid", "updated_at"]