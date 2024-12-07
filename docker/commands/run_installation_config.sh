#!/bin/bash

# Copia configuracion de entorno
cp /code/.config/environment/development/.env_example_docker /code/.config/environment/development/.env &&

sleep 8 &&

pipenv run python /code/manage.py migrate &&

pipenv run python /code/manage.py runserver 0.0.0.0:8000