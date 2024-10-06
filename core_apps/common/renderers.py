import json
from typing import Any, Optional, Union
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class GenericJSONRenderer(JSONRenderer):
    charset = "utf-8"  # Définit l'encodage par défaut
    object_label = "object"  # Label par défaut pour l'objet dans la réponse JSON

    def render(self, data: Union[Any, dict, list],
               accepted_media_type: Optional[str] = None,
               renderer_context: Optional[dict] = None) -> Union[bytes, str]:
        # Initialise le contexte du renderer si non fourni
        if renderer_context is None:
            renderer_context = {}

        # Récupère la vue associée et son label d'objet personnalisé, si défini
        view = renderer_context.get('view')
        object_label = getattr(view, 'object_label', self.object_label)

        # Récupère l'objet response du contexte
        response = renderer_context.get('response')
        if not response:
            # Lève une exception avec un message explicite si la réponse est absente
            raise ValueError("Response object is missing from renderer context")

        # Extrait le code de statut
        status_code = response.status_code
        # Vérifie la présence d'erreurs dans les données
        errors = data.get("errors")

        if errors is not None:
            # Si des erreurs sont présentes, retourne un format JSON standard
            # incluant le code de statut et les erreurs
            return super().render({"status_code": status_code, "errors": errors})

        # Construction et encodage de la réponse JSON personnalisée
        return json.dumps({
            "status_code": status_code,
            object_label: data
        }).encode(self.charset)