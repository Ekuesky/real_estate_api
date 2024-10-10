import os
from os import getenv, path
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = os.path.join(BASE_DIR, "core_apps")

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# Quick-start development settings - unsuitable for production

# Application definition

DJANGO_APPS = [
    "admin_interface",
    "colorfield",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",
    "djoser",
    "social_django",
    "taggit",
    "django_filters",
    "djcelery_email",
    "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.users",
    "core_apps.profiles",
    "core_apps.apartments",
    "core_apps.issues",
    # "core_apps.reports",
    # "core_apps.posts",
    # "core_apps.ratings",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

X_FRAME_OPTIONS = "SAMEORIGIN"              # allows you to use modals insated of popups
SILENCED_SYSTEM_CHECKS = ["security.W019"]  # ignores redundant warning messages

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(APPS_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_DB"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST"),
        "PORT": getenv("POSTGRES_PORT"),
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lome"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

ADMIN_URL = "hidden/"

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

CELERY_TASK_SEND_SENT_EVENT = True
CELERY_RESULT_EXTENDED = True

CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

CELERY_TASK_TIME_LIMIT = 5 * 60

CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_WORKER_SEND_TASK_EVENTS = True

CELERY_BEAT_SCHEDULE = {
    "update-reputations-every-day": {
        "task": "update_reputation_score",
    }
}
# Nom du cookie utilisé pour l'accès
COOKIE_NAME = "access"
# Paramètre SameSite du cookie, défini sur "Lax" pour une sécurité modérée
COOKIE_SAMESITE = "Lax"
# Chemin du cookie, défini sur "/" pour qu'il soit accessible sur tout le site
COOKIE_PATH = "/"
# Empêche l'accès au cookie via JavaScript, renforçant la sécurité
COOKIE_HTTPONLY = True
# Détermine si le cookie doit être envoyé uniquement via HTTPS
# La valeur est lue depuis une variable d'environnement, avec "True" comme valeur par défaut
COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True"

REST_FRAMEWORK = {
    # Définit la classe d'authentification par défaut pour l'API, Utilise une classe personnalisée CookieAuthentication pour l'authentification
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core_apps.common.cookie_auth.CookieAuthentication",
    ),
    # Définit la classe de permission par défaut, Requiert que l'utilisateur soit authentifié pour accéder à l'API
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),

    # Spécifie la classe de pagination par défaut
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",

    # Utilise DjangoFilterBackend pour permettre le filtrage des résultats
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 10,

    # Spécifie les classes de limitation de débit (throttling) par défaut
    # Applique des limites différentes pour les utilisateurs anonymes et authentifiés
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),

    # Les utilisateurs anonymes sont limités à 200 requêtes par jour
    # Les utilisateurs authentifiés sont limités à 500 requêtes par jour
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/day",
        "user": "500/day",
    },
}

SIMPLE_JWT = {
    "SIGNING_KEY": getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "USER_ID_FIELD": "id",
    # Spécifie la clé utilisée dans le payload du JWT pour stocker l'identifiant de l'utilisateur
    "USER_ID_CLAIM": "user_id",
}

DJOSER = {
    # Spécifie le champ utilisé comme identifiant unique de l'utilisateur
    "USER_ID_FIELD": "id",

    # Définit le champ utilisé pour l'authentification (ici, l'email)
    "LOGIN_FIELD": "email",

    # Désactive le modèle de token par défaut de Djoser
    "TOKEN_MODEL": None,

    # Oblige l'utilisateur à saisir deux fois le mot de passe lors de la création du compte
    "USER_CREATE_PASSWORD_RETYPE": True,

    # Active l'envoi d'un email d'activation lors de la création du compte
    "SEND_ACTIVATION_EMAIL": True,

    # Envoie un email de confirmation lorsqu'un mot de passe est changé
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,

    # Oblige l'utilisateur à saisir deux fois le nouveau mot de passe lors de la réinitialisation
    "PASSWORD_RESET_CONFIRM_RETYPE": True,

    # URL pour l'activation du compte (à compléter côté frontend)
    "ACTIVATION_URL": "activate/{uid}/{token}",

    # URL pour la confirmation de réinitialisation du mot de passe (à compléter côté frontend)
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",

    # Liste des URIs autorisés pour la redirection après authentification sociale
    # Récupérée depuis une variable d'environnement et séparée par des virgules
    "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": getenv("REDIRECT_URIS", "").split(","),

    # Sérializers personnalisés pour la création d'utilisateur et l'utilisateur courant
    "SERIALIZERS": {
        "user_create": "core_apps.users.serializers.CreateUserSerializer",
        "current_user": "core_apps.users.serializers.CustomUserSerializer",
    },
}

# Définit la clé client Google OAuth2 à partir de la variable d'environnement GOOGLE_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = getenv("GOOGLE_CLIENT_ID")

# Définit le secret client Google OAuth2 à partir de la variable d'environnement GOOGLE_CLIENT_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = getenv("GOOGLE_CLIENT_SECRET")

# Définit les scopes d'autorisation Google OAuth2 requis (accès à l'email, au profil et à l'openid)
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]
# Définit les données supplémentaires à extraire du profil Google (prénom et nom)
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = ["first_name", "last_name"]

SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "core_apps.profiles.pipeline.save_profile",
]

AUTHENTICATION_BACKENDS = [
    "social_core.backends.google.GoogleOAuth2", # Google OAuth
    "django.contrib.auth.backends.ModelBackend", #default
]