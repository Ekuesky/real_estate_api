from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-z=%v8my#l%p&+2s7ip&d@^uy8t%eh88w!^k0@_)##e9s)g!4sb",
)

LOGGING ={
    "version": 1,
    "disable_existing_loggers": False, #don't disable existing loggers
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-20s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}