# Indian Creek Cycles - Django Bike Rental Platform

A complete, production-ready Django web application for a bike rental business. Features include bike inventory management, online reservations, waiver signing, simulated payments, customer reviews, and weather integration.

## Team Members

* Katie Garcia 

* Katie Elder

* Abdel Mahouel

* Walid Mouhab 
  
## Features

### Customer Features
- **Browse Bikes** - View available bikes by category (Adult, Kids, Mountain)
- **Bike Details** - See specifications, pricing, and compatible accessories
- **Online Reservations** - Book bikes with date selection and accessory add-ons
- **Waiver Signing** - Digital waiver acceptance before rental
- **Simulated Payments** - Complete reservation with demo payment processing
- **Weather Widget** - Check weather by ZIP code for ride planning
- **Trail Information** - Browse local trails with difficulty ratings
- **Customer Reviews** - Submit and read reviews
- **User Accounts** - Registration, login, profile management

### Admin Features
- **Bike Management** - Add, edit, and manage bike inventory
- **Reservation Management** - View and manage all reservations
- **Waiver Records** - Track signed waivers
- **Payment Records** - View simulated payment transactions
- **Review Moderation** - Approve and feature customer reviews
- **Contact Inquiries** - Manage customer inquiries

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, can be changed to PostgreSQL)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with CSS Variables
- **Fonts**: Playfair Display (headings), Inter (body)
- **Icons**: SVG icons

## Project Structure

```
indian_creek_cycles/
├── config/                 # Django project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── core/                   # Core app (homepage, about, contact, trails, weather)
│   ├── models.py          # ContactInquiry, Trail, SiteSetting models
│   ├── views.py           # Home, about, trails, contact, weather API views
│   ├── forms.py           # ContactForm, WeatherZipForm
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── accounts/               # User accounts app
│   ├── models.py          # Custom User model
│   ├── views.py           # Registration, login, profile views
│   ├── forms.py           # UserRegistrationForm, UserProfileForm
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── bikes/                  # Bike inventory app
│   ├── models.py          # BikeCategory, BikeSize, Bike, Accessory models
│   ├── views.py           # Bike listing, detail, category views
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── reservations/           # Reservations app
│   ├── models.py          # Reservation, Waiver, PromoCode models
│   ├── views.py           # Reservation creation, waiver, cancellation views
│   ├── forms.py           # ReservationForm, WaiverForm
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── payments/               # Payments app
│   ├── models.py          # Payment, PaymentMethod models
│   ├── views.py           # Payment processing views
│   ├── forms.py           # PaymentForm
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── reviews/                # Reviews app
│   ├── models.py          # Review, ReviewImage, ReviewHelpfulVote models
│   ├── views.py           # Review listing, submission views
│   ├── forms.py           # ReviewForm
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin configuration
├── templates/              # Django templates
│   ├── base.html          # Base template
│   ├── core/              # Core app templates
│   ├── accounts/          # Accounts app templates
│   ├── bikes/             # Bikes app templates
│   ├── reservations/      # Reservations app templates
│   ├── payments/          # Payments app templates
│   └── reviews/           # Reviews app templates
|   └── admin_dashboard/    # Custom admin dashboard templates
│       ├── base.html       # Admin dashboard base template
│       ├── admin.html      # Dashboard overview
│       ├── admin_bikes.html
│       ├── admin_reservations.html
│       ├── admin_reviews.html
│       └── admin_payments.html
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── images/            # Images
│   └── video/             # Video files
├── media/                  # User-uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env.example           # Environment variables template
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
Make script executable (only needed once):
chmod +x setup.sh

Run setup:
./setup.sh

### Alternative Setup

bash setup.sh
```

The application will be available at: **http://127.0.0.1:8000/**

### Step 7: Access Admin Panel (Optional)

Navigate to: **http://127.0.0.1:8000/admin/**

Login with:
- Username: `admin`
- Password: `admin123`

## Default Users

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser/Admin |
| john_doe | demo123 | Regular user |
| jane_smith | demo123 | Regular user |
| mike_johnson | demo123 | Regular user |
| sarah_williams | demo123 | Regular user |

## URL Routes

### Public Pages
- `/` - Homepage
- `/about/` - About page
- `/trails/` - Trails listing
- `/contact/` - Contact form
- `/bikes/` - Bike listing
- `/bikes/adults/` - Adult bikes
- `/bikes/kids/` - Kids bikes
- `/bikes/mountain/` - Mountain bikes
- `/bikes/sizes/` - Bike size guide
- `/bikes/<slug>/` - Bike detail page
- `/reviews/` - Reviews listing

### Account Pages
- `/accounts/login/` - Login
- `/accounts/register/` - Registration
- `/accounts/logout/` - Logout
- `/accounts/profile/` - User profile
- `/accounts/profile/edit/` - Edit profile

### Reservation Pages (Login Required)
- `/reservations/create/<bike_slug>/` - Create reservation
- `/reservations/waiver/<reservation_id>/` - Sign waiver
- `/reservations/my-reservations/` - My reservations
- `/reservations/detail/<pk>/` - Reservation detail
- `/reservations/cancel/<pk>/` - Cancel reservation
- `/reservations/confirmation/<pk>/` - Reservation confirmation

### Payment Pages (Login Required)
- `/payments/process/<reservation_id>/` - Process payment
- `/payments/confirmation/<payment_id>/` - Payment confirmation
- `/payments/history/` - Payment history

### Admin Dashboard Pages (Staff/Superuser Only)
- `/admin-dashboard/` - Admin dashboard overview
- `/admin-dashboard/bikes/` - Manage bikes
- `/admin-dashboard/reservations/` - Manage reservations
- `/admin-dashboard/reviews/` - Moderate reviews
- `/admin-dashboard/payments/` - View/manage payments
- `/admin-dashboard/bikes/<bike_id>/toggle-availability/` - Toggle bike availability
- `/admin-dashboard/bikes/<bike_id>/toggle-maintenance/` - Toggle bike maintenance
- `/admin-dashboard/reservations/<reservation_id>/status/<new_status>/` - Update reservation status
- `/admin-dashboard/reviews/<review_id>/approve/` - Approve review
- `/admin-dashboard/reviews/<review_id>/unapprove/`- Unapprove review
- `/admin-dashboard/payments/<payment_id>/refund/` - Refund payment
- `/admin-dashboard/payments/<payment_id>/void/` - Void payment

### API Endpoints
- `/api/weather/?zip_code=<zip>` - Get weather data
- `/reservations/check-availability/?bike_id=<id>&date=<date>` - Check bike availability

## Weather API Configuration

The weather feature works in two modes:

### Demo Mode (Default)
Without an API key, the weather endpoint returns mock data for demonstration purposes.

### Live Mode (With OpenWeather API)
1. Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api)
2. Add the key to your `.env` file:
   ```
   OPENWEATHER_API_KEY=your-api-key-here
   ```
3. Restart the server

## Customization

### Adding a Homepage Video

1. Place your video file in `static/video/`
2. Name it `family-biking.mp4` (or update the reference in `templates/core/home.html`)
3. The video should be:
   - MP4 format
   - Optimized for web (compressed)
   - Family-friendly cycling content

### Changing Colors

Edit CSS variables in `static/css/main.css`:

```css
:root {
    --color-primary: #1a472a;      /* Dark green */
    --color-primary-dark: #0d2916; /* Darker green */
    --color-accent: #c9a227;       /* Gold */
    /* ... other variables */
}
```

### Adding New Bike Categories

1. Log in to the admin panel
2. Go to "Bike Categories"
3. Click "Add Bike Category"
4. Fill in name, slug, and description

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Generate a new `SECRET_KEY`
3. Configure allowed hosts
4. Set up a production database (PostgreSQL recommended)
5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
6. Use a production WSGI server (Gunicorn, uWSGI)
7. Configure a reverse proxy (Nginx, Apache)

## Testing

Run Django tests:

```bash
python manage.py test
```

## License

This project is created for educational purposes.

## Support

For issues or questions, please refer to the Django documentation or contact the project maintainer.

---

# Indian Creek Cycles: Smart-Dock Implementation

# New Features
Functional Smart-Dock System: Integrated the logic required to connect the web application to the physical docking hardware.

Active Unlock/Return Flow: Users can now successfully "Unlock" a bike to begin a session and "Return" it to end the billing cycle.

Access Credentials: Automated generation of dynamic QR Codes and 6-digit manual entry codes for every reservation.

Responsive Interface: A redesigned Reservation Detail page that prioritizes the "Smart-Dock Access" card for easy trailhead use.

# Setup & Installation
Install Required Packages:

pip install qrcode pillow

Apply Database Migrations:

python manage.py migrate

---


**Made with ❤️ for bike lovers**
