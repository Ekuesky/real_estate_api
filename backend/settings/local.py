from os import getenv, path
from dotenv import load_dotenv

load_dotenv()

from .base import BASE_DIR

local_env_file = path.join(BASE_DIR, ".envs", ".env.local")

if path.isfile(local_env_file):
    load_dotenv(local_env_file)

DEBUG = True

SITE_NAME = getenv("SITE_NAME")

SECRET_KEY = getenv(
    "DJANGO_SECRET_KEY", "django-insecure-z=%v8my#l%p&+2s7ip&d@^uy8t%eh88w!^k0@_)##e9s)g!4sb"
)
