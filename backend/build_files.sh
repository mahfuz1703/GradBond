#!/bin/bash

set -e  # Exit on any error

echo "BUILD START"

# Upgrade pip and install requirements
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "BUILD END"
