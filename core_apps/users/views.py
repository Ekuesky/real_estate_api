import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Configuration du logger
logger = logging.getLogger(__name__)


# Fonction pour définir les cookies d'authentification
def set_auth_cookies(response: Response, access_token: str, refresh_token: Optional[str] = None) -> None:
    # Définition de la durée de vie du token d'accès en secondes
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()

    # Définition des paramètres des cookies par defaut
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }

    # Définir le cookie "access" avec le token d'accès et les paramètres
    response.set_cookie("access", access_token, **cookie_settings)

    # Si un token de rafraîchissement est fourni, le définir avec les paramètres appropriés
    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    # Définir un cookie "logged_in" pour indiquer que l'utilisateur est connecté
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


# Vue personnalisée pour obtenir un couple de tokens (d'accès et de rafraîchissement)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Appel de la méthode post de la classe parent pour obtenir les tokens
        token_res = super().post(request, *args, **kwargs)

        # Si la requête a réussi (status code 200)
        if token_res.status_code == status.HTTP_200_OK:
            # Extraire les tokens d'accès et de rafraîchissement de la réponse
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            # Si les deux tokens sont présents
            if access_token and refresh_token:
                # Définir les cookies d'authentification
                set_auth_cookies(
                    token_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Supprimer les clés "access" et "refresh" de la réponse
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)

                # Définir un message de succès
                token_res.data["message"] = "Login Successful."
            else:
                # Définir un message d'erreur si un token est manquant
                token_res.data["message"] = "Login Failed"
                logger.error("Access or refresh token not found in login response data")

        # Retourner la réponse
        return token_res


# Vue personnalisée pour rafraîchir le token d'accès
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Extraire le token de rafraîchissement du cookie
        refresh_token = request.COOKIES.get("refresh")

        # Si le token de rafraîchissement est présent
        if refresh_token:
            # Définir le token de rafraîchissement dans la requête
            request.data["refresh"] = refresh_token

        # Appel de la méthode post de la classe parent pour rafraîchir le token
        refresh_res = super().post(request, *args, **kwargs)

        # Si la requête a réussi (status code 200)
        if refresh_res.status_code == status.HTTP_200_OK:
            # Extraire les tokens d'accès et de rafraîchissement de la réponse
            access_token = refresh_res.data.get("access")
            refresh_token = refresh_res.data.get("refresh")

            # Si les deux tokens sont présents
            if access_token and refresh_token:
                # Définir les cookies d'authentification
                set_auth_cookies(
                    refresh_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Supprimer les clés "access" et "refresh" de la réponse
                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)

                # Définir un message de succès
                refresh_res.data["message"] = "Access tokens refreshed successfully"
            else:
                # Définir un message d'erreur si un token est manquant
                refresh_res.data["message"] = (
                    "Access or refresh tokens not found in refresh response data"
                )
                logger.error(
                    "Access or refresh token not found in refresh response data"
                )

        # Retourner la réponse
        return refresh_res


# Vue personnalisée pour l'authentification via un fournisseur tiers
class CustomProviderAuthView(ProviderAuthView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        # Appel de la méthode post de la classe parent pour l'authentification du fournisseur
        provider_res = super().post(request, *args, **kwargs)

        # Si la requête a réussi (status code 201)
        if provider_res.status_code == status.HTTP_201_CREATED:
            # Extraire les tokens d'accès et de rafraîchissement de la réponse
            access_token = provider_res.data.get("access")
            refresh_token = provider_res.data.get("refresh")

            # Si les deux tokens sont présents
            if access_token and refresh_token:
                # Définir les cookies d'authentification
                set_auth_cookies(
                    provider_res,
                    access_token=access_token,
                    refresh_token=refresh_token,
                )

                # Supprimer les clés "access" et "refresh" de la réponse
                provider_res.data.pop("access", None)
                provider_res.data.pop("refresh", None)

                # Définir un message de succès
                provider_res.data["message"] = "You are logged in Successful."
            else:
                # Définir un message d'erreur si un token est manquant
                provider_res.data["message"] = (
                    "Access or refresh token not found in provider response"
                )
                logger.error(
                    "Access or refresh token not found in provider response data"
                )

        # Retourner la réponse
        return provider_res


# Vue pour la déconnexion
class LogoutAPIView(APIView):
    def post(self, request: Request, *args, **kwargs):
        # Créer une réponse avec un status code 204 (No Content)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        # Supprimer les cookies d'authentification
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        # Retourner la réponse
        return response