
## Team Members

* Katie Garcia 

* Katie Elder

* Abdel Mahouel

* Walid Mouhab

----------------
# Indian Creek Cycles – Django Backend

This project is a Django backend application built with Django and Django REST Framework.

---

## Requirements

- Python 3.10+
- pip

---

## Project Setup (macOS / Linux)

1. Navigate to the project root (the folder containing `manage.py`):

```
cd path/to/project
```

2. Create a virtual environment:

```
python3 -m venv .venv
```

3. Activate the virtual environment:

```
source .venv/bin/activate
```

4. Install project dependencies:

```
python -m pip install -r requirements.txt
```

---

## Database Setup (First Run)

Apply migrations to create the database tables:

```
python manage.py makemigrations pricing
python manage.py migrate
python manage.py showmigrations pricing #confirming prices
```

If you pull new updates later and migrations were added, run this command again.






Create an admin user:

```
python manage.py createsuperuser
Username: 'admin'
Email address: '  '
Password: 'password'

```

---

## Running the Development Server

Start the server:

```
python manage.py runserver
```

Open your browser and go to:

```
http://127.0.0.1:8000/

```

API endpoints:

- /admin/
- /api/pricing/quote/
- /api/pricing/bikes
- /api/pricing/bikes/1
- /api/payments/pay/



## API Endpoints

These endpoints are API endpoints. If you visit them in a browser, the browser sends a **GET** request.
Some endpoints are **POST-only**, so you may see: `{"detail":"Method \"GET\" not allowed."}` — that is expected.

### Pricing
- POST `/api/pricing/quote/` (calculate a pricing quote)
- GET `/api/pricing/bikes/` (list bikes) *(requires database table + data)*
- PUT `/api/pricing/bikes/<bike_id>/` (update a bike)

### Payments
- POST `/api/payments/pay/` (pay for a reservation)
---

## Testing POST endpoints (example)

Use `curl` (or Postman/Insomnia) to send a POST request.

open an ADDITIONAL terminal (leave the previous one running while trying this)

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/pricing/quote/ \
  -H "Content-Type: application/json" \
  -d '{Note: Replace the JSON body with the fields the endpoint expects.}'
  Example: 
  -d '{
        "bike_id": 1,
        "hourly_rate": 30, 
        "start_date": "2026-03-10",
        "end_date": "2026-03-12"
      }'

      OTHER CURL: 

##Testing payment:

curl -X POST http://127.0.0.1:8000/api/payments/pay/ \
  -H "Content-Type: application/json" \
  -d '{
    "reservation_id": 1,
    "amount": 60.00,
    "payment_method": "card"
  }'

##Testing price 

curl -X POST http://127.0.0.1:8000/api/pricing/quote/ \
  -H "Content-Type: application/json" \
  -d '{
    "hourly_rate": 15,
    "start_date": "2026-03-02T10:00:00",
    "end_date": "2026-03-02T14:00:00",
    "promo_code": "SUMMER2026"  
  }' | python3 -m json.tool


## testing payment with curl

curl -i -X POST http://127.0.0.1:8000/api/payments/pay/ \
  -H "Content-Type: application/json" \
  -d '{"reservation_id":2,"amount":"60.00","payment_method":"cash"}'

## Windows Setup

Activate the virtual environment using:

```
.venv\Scripts\activate
```

Then follow the same install and run steps above.

---

## Tech Stack

- Django
- Django REST Framework
- SQLite (default development database)

---

## Updating Dependencies

If new Python packages are added, update the requirements file:

```
python -m pip freeze > requirements.txt
```