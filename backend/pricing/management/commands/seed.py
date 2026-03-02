from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import datetime

from pricing.models import (
    RentalLocation,
    User,
    BikeType,
    Bike,
    Trail,
    Accessory,
    PromoCode,
    Reservation,
)

class Command(BaseCommand):
    help = "Seed the database with sample data."

    def handle(self, *args, **options):
        # --- Rental Location ---
        location, _ = RentalLocation.objects.get_or_create(
            location_name="Indian Creek Cycle Rentals",
            defaults={
                "address": "123 Indian Creek Trailhead",
                "city": "Overland Park",
                "state": "KS",
                "zip_code": "66210",
                "phone_number": "913-555-BIKE",
            },
        )

        # --- Users ---
        users_data = [
            ("Amelia Smith", "amelia.smith@example.com", "password123", "1995-01-15"),
            ("Noah Johnson", "noah.johnson@example.com", "password124", "1992-02-20"),
            ("Olivia Brown", "olivia.brown@example.com", "password125", "1988-03-05"),
            ("Liam Jones", "liam.jones@example.com", "password126", "1990-04-12"),
        ]
        users = []
        for name, email, password, birthday in users_data:
            u, _ = User.objects.get_or_create(
                email=email,
                defaults={"name": name, "password": password, "birthday": birthday},
            )
            users.append(u)

        # --- Bike Types ---
        bike_types_data = [
            ("Balance Bike", "Lightweight for kids"),
            ("Childrens Bike", "Aged 5-12"),
            ("BMX Bike", "For tricks"),
            ("Mountain Bike", "Off-road adventures"),
            ("Standard Adult", "City commuting"),
            ("Comfort Cruiser", "Leisurely rides"),
            ("Hybrid Bike", "Fitness and commuting"),
            ("Electric-Assist", "Battery powered boost"),
            ("Tandem Bike", "For two people"),
            ("Cargo Bike", "For carrying heavy loads"),
        ]
        bike_types = []
        for type_name, desc in bike_types_data:
            bt, _ = BikeType.objects.get_or_create(type_name=type_name, defaults={"description": desc})
            bike_types.append(bt)

        # --- Trails (20) ---
        trails_data = [
            ("Blue River Trail", 5.0, "Easy", "Scenic river views."),
            ("Kill Creek Park Trail", 3.5, "Moderate", "Wooded areas and open fields."),
            ("Shawnee Mission Park Trail", 7.2, "Moderate", "Varied terrains."),
            ("Indian Creek Trail", 4.8, "Easy", "Paved trail."),
            ("Mill Creek Streamway Park", 6.0, "Easy", "Alongside Mill Creek."),
            ("Lenexa Lake Trail", 2.1, "Easy", "Loop around the lake."),
            ("Heritage Park Trail", 5.5, "Moderate", "Beautiful landscapes."),
            ("Olathe Lake Trail", 4.0, "Easy", "Flat trail."),
            ("De Soto Riverfront Park Trail", 3.2, "Easy", "Along the Kansas River."),
            ("Cedar Creek Trail", 8.0, "Difficult", "Steep and rocky."),
            ("Prairie Center Trail", 5.5, "Moderate", "Prairie and woods."),
            ("Riverview Park Trail", 3.0, "Easy", "Short river trail."),
            ("Weston Bend State Park Trail", 6.8, "Difficult", "Rugged river views."),
            ("Swope Park Trail", 4.3, "Moderate", "Flat and hilly."),
            ("Briarwood Trail", 2.8, "Easy", "Residential area."),
            ("Black Hoof Park Trail", 3.7, "Easy", "Family-friendly."),
            ("JCCC Trail", 5.0, "Moderate", "College campus."),
            ("Antioch Park Trail", 4.5, "Moderate", "Ponds and wildlife."),
            ("Yardley Park Trail", 3.3, "Easy", "Flat leisure trail."),
            ("Tomahawk Creek Trail", 6.0, "Moderate", "Picturesque creek."),
        ]
        trails = []
        for name, dist, diff, desc in trails_data:
            t, _ = Trail.objects.get_or_create(
                name=name,
                defaults={
                    "distance": Decimal(str(dist)),
                    "difficulty": diff,
                    "description": desc,
                },
            )
            trails.append(t)

        # --- Bikes (example 5 like your SQL) ---
        bikes_data = [
            (bike_types[0], "One Size", Decimal("15.00"), "Available"),
            (bike_types[1], "Small", Decimal("10.00"), "Available"),
            (bike_types[1], "Medium", Decimal("12.00"), "Rented"),
            (bike_types[2], "Small", Decimal("12.00"), "Available"),
            (bike_types[3], "Medium", Decimal("18.00"), "Available"),
        ]
        bikes = []
        for bt, size, rate, status in bikes_data:
            b, _ = Bike.objects.get_or_create(
                type=bt,
                location=location,
                size=size,
                hourly_rate=rate,
                defaults={"status": status},
            )
            # If it already existed, update status to keep consistent
            if b.status != status:
                b.status = status
                b.save()
            bikes.append(b)

        # --- Accessories ---
        accessories_data = [
            ("Helmet", Decimal("50.00"), "Safety first!"),
            ("Water Bottle", Decimal("10.00"), "Stay hydrated."),
            ("Bike Lock", Decimal("25.00"), "Secure your ride."),
            ("Bike Bag", Decimal("15.00"), "Carry essentials."),
            ("Cycling Gloves", Decimal("20.00"), "Comfortable grip."),
            ("Repair Kit", Decimal("12.00"), "Essential tools."),
            ("Portable Pump", Decimal("22.00"), "For inflating tires."),
            ("Reflective Vest", Decimal("20.00"), "Visibility and safety."),
            ("Saddle Bag", Decimal("18.00"), "Storage."),
            ("Bike Lights", Decimal("15.00"), "LED visibility."),
        ]
        for name, price, desc in accessories_data:
            Accessory.objects.get_or_create(name=name, defaults={"price": price, "description": desc})

        # --- Promo Codes ---
        promo_data = [
            ("SUMMER2026", "Get 20% off your next bike rental!", "2026-09-01", True),
            ("FALL2026", "15% discount on rentals for the fall season.", "2026-12-01", True),
            ("WEEKENDDEAL", "Rent any bike on the weekend and get 10% off.", "2026-09-30", True),
            ("FREEHOUR", "Rent for 2 hours and get the 3rd hour free!", "2026-10-15", True),
            ("FIRSTRENTAL", "20% off for first-time renters.", "2026-12-31", True),
            ("GROUPDISCOUNT", "Rent 3 bikes or more and get 25% off!", "2026-11-15", True),
            ("MEMBEREXCLUSIVE", "Exclusive 30% off for members.", "2026-12-31", True),
            ("HOLIDAYSALE", "Celebrate the holidays with 15% off all rentals.", "2026-12-25", True),
            ("WINTER2026", "10% off rentals during the winter months.", "2027-03-01", True),
            ("REFERAFRIEND", "Refer a friend and both get 10% off your next rental!", "2026-09-30", True),
            ("BIRTHDAYFREE", "Enjoy a free ride for your birthday to use anytime!", "2026-12-31", True),
        ]
        for code, desc, exp, active in promo_data:
            PromoCode.objects.get_or_create(
                code=code,
                defaults={"description": desc, "expiry_date": exp, "is_active": active},
            )

        # --- One sample reservation like your SQL ---
        Reservation.objects.get_or_create(
            reservation_id=1,
            defaults={
                "user": users[0],
                "bike": bikes[0],
                "trail": trails[0],
                "location": location,
                "start_date": datetime(2026, 3, 1, 10, 0, 0),
                "end_date": datetime(2026, 3, 1, 12, 0, 0),
                "total_cost": Decimal("20.00"),
                "status": "Completed",
                "rating": 5,
                "review_text": "Loved it!",
                "booking_date": timezone.now(),
            },
        )

        self.stdout.write(self.style.SUCCESS("✅ Seed complete. Check /admin/ for data."))