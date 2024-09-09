from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-z=%v8my#l%p&+2s7ip&d@^uy8t%eh88w!^k0@_)##e9s)g!4sb",
)
