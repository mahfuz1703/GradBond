#!/bin/bash

set -e  # Exit on error

echo "BUILD START"

# Use the specific version of Python
python3.9 -m pip install --upgrade pip
python3.9 -m pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --noinput --clear

echo "BUILD END"
