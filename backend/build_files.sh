#!/bin/bash
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
python3 manage.py makemigrations
python3 manage.py migrate
daphne -b 0.0.0.0 -p $PORT GradBond.asgi:application
