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
