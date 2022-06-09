SHELL := /bin/bash

manage_py := docker exec -it backend python app/manage.py

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver 0:8001

gunicorn:
	 cd app && gunicorn settings.wsgi --threads 2 --workers 4 --log-level debug --max-requests 1000 --timeout 10 --bind=0.0.0.0:8000

uwsgi:
	cd app && uwsgi --http :8000 --module settings.wsgi --threads 2 --workers 4 --socket 0.0.0.0:8080

run-dev: migrate \
	run

worker:
	cd app && celery -A settings worker -l info --autoscale 1,10

beat:
	cd app && celery -A settings beat -l info

pytest:
	docker exec -it backend pytest ./app/tests --cov=app --cov-report html -vv && coverage report --fail-under=67

flake8:
	docker exec -it backend flake8 app/