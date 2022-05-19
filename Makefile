SHELL := /bin/bash

manage_py := python3 app/manage.py

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

shell:
	$(manage_py) shell_plus --print-sql

run:
	$(manage_py) runserver

run-dev: migrate \
	run

worker:
	cd app && celery -A settings worker -l info --autoscale 1,10

beat:
	cd app && celery -A settings beat -l info

pytest:
	pytest ./app/tests --cov=app --cov-report html -vv && coverage report --fail-under=76

