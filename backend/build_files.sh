#!/bin/bash
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
daphne GradBond.asgi:application
