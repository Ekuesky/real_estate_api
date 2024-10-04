import os
from os import getenv, path
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = os.path.join(BASE_DIR, "core_apps")


local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Application definition

DJANGO_APPS = [
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
    # "djoser",
    # "social_django",
    # "taggit",
    "django_filters",
    # "djcelery_email",
    # "django_celery_beat",
]

LOCAL_APPS = [
    "core_apps.common",
    "core_apps.users",
    "core_apps.profiles",
    # "core_apps.ratings",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lome"

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

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
        "task": "update_all_reputations",
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

# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         "core_apps.common.cookie_auth.CookieAuthentication",
#     ),
#     "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "DEFAULT_FILTER_BACKENDS": [
#         "django_filters.rest_framework.DjangoFilterBackend",
#     ],
#     "PAGE_SIZE": 10,
#     "DEFAULT_THROTTLE_CLASSES": (
#         "rest_framework.throttling.AnonRateThrottle",
#         "rest_framework.throttling.UserRateThrottle",
#     ),
#     "DEFAULT_THROTTLE_RATES": {
#         "anon": "200/day",
#         "user": "500/day",
#     },
# }
#
# SIMPLE_JWT = {
#     "SIGNING_KEY": getenv("SIGNING_KEY"),
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": True,
#     "USER_ID_FIELD": "id",
#     "USER_ID_CLAIM": "user_id",
# }
#
# DJOSER = {
#     "USER_ID_FIELD": "id",
#     "LOGIN_FIELD": "email",
#     "TOKEN_MODEL": None,
#     "USER_CREATE_PASSWORD_RETYPE": True,
#     "SEND_ACTIVATION_EMAIL": True,
#     "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
#     "PASSWORD_RESET_CONFIRM_RETYPE": True,
#     "ACTIVATION_URL": "activate/{uid}/{token}",
#     "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
#     "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": getenv("REDIRECT_URIS", "").split(","),
#     "SERIALIZERS": {
#         "user_create": "core_apps.users.serializers.CreateUserSerializer",
#         "current_user": "core_apps.users.serializers.CustomUserSerializer",
#     },
# }