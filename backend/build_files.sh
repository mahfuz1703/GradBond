#!/bin/bash

set -e  # Exit on error

echo "BUILD START"

echo "Python Version:"
python --version || echo "Python not found"

echo "Pip Version:"
pip --version || echo "Pip not found"

echo "Installing dependencies..."
pip install -r requirements.txt || echo "Dependency installation failed"

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static collection failed"

echo "BUILD END"
