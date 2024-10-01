config:
	docker compose -f local.yml config

build:
	#docker buildx create --use
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

down-v:
	docker compose -f local.yml down -v

show-logs:
	docker compose -f local.yml logs

show-logs-api:
	docker compose -f local.yml logs api

makemigrations:
	docker compose -f local.yml run --rm api python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm api python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm api python manage.py createsuperuser

db-volume:
	docker volume inspect api_estate_prod_postgres_data

mailpit-volume:
	docker volume inspect api_estate_prod_mailpit_data

estate-db:
	docker compose -f local.yml exec postgres psql --username=alphaogilo --dbname=estate

shell:
	docker compose -f local.yml exec api python manage.py shell

rmi-dangling:
	@echo "Removing dangling images ..."
	docker images --filter "dangling=true" -q | xargs docker rmi

rmi-all:
	@echo "Removing all images ..."
	docker rmi $(docker images -q)

empty-docker:
	@echo "Emptying docker"
	docker system prune -a --volumes -f

signing-key:
	python -c "import secrets; print(secrets.token_urlsafe(38))"

test-cov-html:
	docker compose -f local.yml run --rm api pytest -p no:warnings --cov=. --cov-report html

test-cov-verbose:
	docker compose -f local.yml run --rm api pytest -p no:warnings --cov=. -v

create-index:
	docker compose -f local.yml run --rm api python manage.py search_index --create

populate-index:
	docker compose -f local.yml run --rm api python manage.py search_index --populate

rebuild-index:
	docker compose -f local.yml run --rm api python manage.py search_index --rebuild