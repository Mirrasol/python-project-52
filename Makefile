install:
	poetry install

dev:
	poetry run python manage.py runserver

start:
	poetry run python -m gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell

lint:
	poetry run flake8 task_manager

messages:
	poetry run django-admin makemessages -l ru

compile:
	poetry run django-admin compilemessages

tests:
	poetry run python manage.py test task_manager.tests