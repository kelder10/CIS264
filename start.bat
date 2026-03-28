@echo off
REM Indian Creek Cycles - Quick Start Script for Windows
REM This script sets up and runs the Django development server

echo ==========================================
echo Indian Creek Cycles - Quick Start
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
)

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Seed database
echo Seeding database with sample data...
python manage.py seed

echo.
echo ==========================================
echo Starting development server...
echo ==========================================
echo.
echo Access the website at: http://127.0.0.1:8000
echo Admin panel: http://127.0.0.1:8000/admin
echo.
echo Default login credentials:
echo   Admin: admin / admin123
echo   Users: john_doe / demo123 (or jane_smith, mike_johnson, sarah_williams)
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

REM Deactivate virtual environment on exit
call deactivate
