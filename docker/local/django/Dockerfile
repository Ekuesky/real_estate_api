FROM docker.io/python:3.12.2-slim-bookworm as python

# Etape 1: Build our dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local
#Met à jour les paquets et installe les outils de compilation et la bibliothèque PostgreSQL.
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

COPY ./requirements .

#Crée des wheels Python pour les dépendances listées dans le fichier correspondant à BUILD_ENVIRONMENT.
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt

# Etape 2: Python run stage.
FROM python as python-run-stage
ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

# Configure des variables d'environnement Python.
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV BUILD_ENV ${BUILD_ENVIRONMENT}
# Définit le répertoire de travail.
WORKDIR ${APP_HOME}
# Installe des outils supplémentaires.
RUN apt-get update && apt-get install --no-install-recommends -y \
  sudo git bash-completion nano ssh

# Crée un utilisateur et un groupe "django", et configure les permissions pour les fichiers statiques.
RUN addgroup --system django && \
  adduser --system --ingroup django django && \
  mkdir -p ${APP_HOME}/staticfiles && \
  chown django:django ${APP_HOME}/staticfiles && \
  chmod 775 ${APP_HOME}/staticfiles \

# Installe des dépendances supplémentaires et nettoie le cache APT.
RUN apt-get update && apt-get install --no-install-recommends -y \
  libpq-dev \
  gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copie les wheels Python créés dans l'étape précédente.
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Installe les wheels Python et supprime le dossier wheels.
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copie le script d'entrée, corrige les fins de ligne et le rend exécutable.
COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY --chown=django:django ./docker/local/django/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


# Copie le reste des fichiers de l'application dans le conteneur.
COPY --chown=django:django . ${APP_HOME}

# Change le propriétaire du répertoire de l'application
RUN chown django:django ${APP_HOME}

# Bascule vers l'utilisateur django.
USER django

# Définit le point d'entrée du conteneur.
ENTRYPOINT [ "/entrypoint" ]

