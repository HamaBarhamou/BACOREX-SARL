#!/usr/bin/env bash

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

rm db.sqlite3

python manage.py makemigrations
python manage.py makemigrations polls
python manage.py makemigrations gestioncouriers
python manage.py makemigrations userprofile
python manage.py makemigrations gestionprojets
python manage.py migrate