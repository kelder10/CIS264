#!/bin/bash

set -ex

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3.12 -m venv .venv
fi

echo "### Step 1: Activate Virtual Environment"
source .venv/bin/activate

echo "### Step 2: Upgrade pip tools"
python -m pip install --upgrade pip setuptools wheel

echo "### Step 3: Install Dependencies"
python -m pip install -r requirements.txt

echo "### Step 4: Ensure django-anymail is installed"
if ! python -c "import anymail" &> /dev/null; then
  echo "Installing django-anymail..."
  python -m pip install django-anymail
else
  echo "django-anymail already installed"
fi

echo "### Step 5: Configure Environment Variables"
if [ -f ".env.example" ]; then
  if [ ! -f ".env" ]; then
    cp .env.example .env
  else
    echo ".env already exists, skipping copy"
  fi
else
  touch .env
fi

echo "### Step 6: Run Database Migrations"
python manage.py makemigrations
echo "Running migrations..."
python manage.py migrate

echo "### Step 7: Seed Database with Sample Data"
cat <<'EOF'
This creates:
- Admin user (username: admin, password: admin123)
- Sample users (password: demo123)
- Bike categories and sizes
- Sample bikes (11 bikes across categories)
- Accessories (helmets, locks, baskets, etc.)
- Sample trails (5 trails)
- Promo codes (WELCOME20, FAMILY10, WEEKEND15)
- Sample reviews (6 reviews)
EOF

python manage.py seed

echo "### Step 8: Run Development Server"
python manage.py runserver