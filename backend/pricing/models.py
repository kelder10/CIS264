from django.db import models

# Create your models here.



class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="userid")
    name = models.CharField(max_length=100, db_column="name")
    email = models.CharField(max_length=100, unique=True, db_column="email")
    password = models.CharField(max_length=100, db_column="password")
    birthday = models.DateField(null=True, blank=True, db_column="birthday")

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.name} ({self.email})"


class RentalLocation(models.Model):
    location_id = models.AutoField(primary_key=True, db_column="locationid")
    location_name = models.CharField(max_length=100, db_column="locationname")
    address = models.CharField(max_length=255, db_column="address")
    city = models.CharField(max_length=100, db_column="city")
    state = models.CharField(max_length=2, db_column="state")
    zip_code = models.CharField(max_length=10, db_column="zipcode")
    phone_number = models.CharField(max_length=20, null=True, blank=True, db_column="phonenumber")

    class Meta:
        db_table = "rentallocations"

    def __str__(self):
        return self.location_name


class BikeType(models.Model):
    type_id = models.AutoField(primary_key=True, db_column="typeid")
    type_name = models.CharField(max_length=50, db_column="typename")
    
    # --- YOUR ADDITION ---
    CATEGORY_CHOICES = [('Adult', 'Adult'), ('Kids', 'Kids')]
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='Adult')
    # ---------------------

    description = models.TextField(null=True, blank=True, db_column="description")

    class Meta:
        db_table = "biketypes"

    def __str__(self):
        return f"{self.type_name} ({self.category})"


class Trail(models.Model):
    trail_id = models.AutoField(primary_key=True, db_column="trailid")
    name = models.CharField(max_length=100, db_column="name")
    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column="distance")
    difficulty = models.CharField(max_length=20, null=True, blank=True, db_column="difficulty")
    description = models.TextField(null=True, blank=True, db_column="description")
    zip_code = models.CharField(max_length=10, null=True, blank=True, db_column="zipcode")

    class Meta:
        db_table = "trails"

    def __str__(self):
        return self.name
    

class Bike(models.Model):
    bike_id = models.AutoField(primary_key=True, db_column="bikeid")
    # Added 'name' to give bikes identity (e.g. "Red Cruiser")
    name = models.CharField(max_length=100, db_column="name", default="Standard Bike")
    
    type = models.ForeignKey(BikeType, on_delete=models.PROTECT, db_column="typeid")
    location = models.ForeignKey(RentalLocation, on_delete=models.PROTECT, db_column="locationid")
    size = models.CharField(max_length=20, null=True, blank=True, db_column="size")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, db_column="hourlyrate")
    status = models.CharField(max_length=20, default="Available", db_column="status")
    
    # --- ADDITION ---
    is_available = models.BooleanField(default=True, db_column="available")
    # ---------------------

    class Meta:
        db_table = "bikes"

    def __str__(self):
        return f"{self.name} ({self.size})"


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True, db_column="reservationid")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, db_column="userid")
    bike = models.ForeignKey(Bike, on_delete=models.SET_NULL, null=True, blank=True, db_column="bikeid")
    trail = models.ForeignKey(Trail, on_delete=models.SET_NULL, null=True, blank=True, db_column="trailid")
    location = models.ForeignKey(RentalLocation, on_delete=models.SET_NULL, null=True, blank=True, db_column="locationid")

    start_date = models.DateTimeField(db_column="startdate")
    end_date = models.DateTimeField(db_column="enddate")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column="totalcost")
    status = models.CharField(max_length=20, default="Upcoming", db_column="status")
    rating = models.IntegerField(null=True, blank=True, db_column="rating")
    review_text = models.TextField(null=True, blank=True, db_column="reviewtext")
    booking_date = models.DateTimeField(auto_now_add=False, db_column="bookingdate")

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"Reservation {self.reservation_id} ({self.status})"
    
class Accessory(models.Model):
    accessory_id = models.AutoField(primary_key=True, db_column="accessoryid")
    name = models.CharField(max_length=100, db_column="name")
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column="price")
    description = models.TextField(null=True, blank=True, db_column="description")

    class Meta:
        db_table = "accessories"
        verbose_name_plural = "Accessories"
    def __str__(self):
        return f"{self.name} (${self.price})"


class PromoCode(models.Model):
    promo_code_id = models.AutoField(primary_key=True, db_column="promocodeid")
    code = models.CharField(max_length=50, unique=True, db_column="code")
    description = models.TextField(null=True, blank=True, db_column="description")
    expiry_date = models.DateField(null=True, blank=True, db_column="expirydate")
    is_active = models.BooleanField(default=True, db_column="isactive")

    class Meta:
        db_table = "promocodes"

    def __str__(self):
        return self.code
    
    