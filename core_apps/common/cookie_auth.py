import logging
from typing import Optional, Tuple
from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token

# Configuration du logger pour cette classe
logger = logging.getLogger(__name__)


class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        # Tente d'obtenir le header d'authentification
        header = self.get_header(request)
        raw_token = None

        # Si un header est présent, extrait le token brut
        if header is not None:
            raw_token = self.get_raw_token(header)

        # Sinon, vérifie si le token est présent dans les cookies
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)

        # Si un token brut a été trouvé (soit dans le header, soit dans les cookies)
        if raw_token is not None:
            try:
                # Valide le token
                validated_token = self.get_validated_token(raw_token)
                # Retourne l'utilisateur associé au token et le token validé
                return self.get_user(validated_token), validated_token

            except TokenError as e:
                # En cas d'erreur de validation du token, log l'erreur
                logger.error(f"Token validation error: {str(e)}")

        # Si aucun token valide n'a été trouvé, retourne None
        return None