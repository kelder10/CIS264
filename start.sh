#!/bin/bash

# Indian Creek Cycles - Quick Start Script
# This script sets up and runs the Django development server

echo "=========================================="
echo "Indian Creek Cycles - Quick Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Seed database if it's empty
echo "Checking if database needs seeding..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from bikes.models import Bike
if Bike.objects.count() == 0:
    print('Seeding database...')
    from django.core.management import call_command
    call_command('seed')
else:
    print('Database already seeded.')
"

echo ""
echo "=========================================="
echo "Starting development server..."
echo "=========================================="
echo ""
echo "Access the website at: http://127.0.0.1:8000"
echo "Admin panel: http://127.0.0.1:8000/admin"
echo ""
echo "Default login credentials:"
echo "  Admin: admin / admin123"
echo "  Users: john_doe / demo123 (or jane_smith, mike_johnson, sarah_williams)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
