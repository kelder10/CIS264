#!/bin/bash

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3.12 -m venv .venv
fi

echo "### Step 1: Create Virtual Environment"
source .venv/bin/activate

echo "### Step 2: Install Dependencies"
pip install -r requirements.txt

echo "### Step 3: Configure Environment Variables"
cp -n .env.example .env

echo "### Step 4: Run Database Migrations"
python manage.py makemigrations

echo "Running migrations..."
python manage.py migrate

echo "### Step 5: Seed Database with Sample Data"
echo "
This creates:
- Admin user (username: `admin`, password: `admin123`)
- Sample users (password: `demo123`)
- Bike categories and sizes
- Sample bikes (11 bikes across categories)
- Accessories (helmets, locks, baskets, etc.)
- Sample trails (5 trails)
- Promo codes (WELCOME20, FAMILY10, WEEKEND15)
- Sample reviews (6 reviews)"

python manage.py seed

echo "### Step 6: Run Development Server"

python manage.py runserver