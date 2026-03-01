-------------------------------------------------------------------------------
-- 1. CREATE TABLES (The Structure)
-------------------------------------------------------------------------------

CREATE TABLE Users (
UserID SERIAL PRIMARY KEY,
Name VARCHAR(100) NOT NULL,
Email VARCHAR(100) UNIQUE NOT NULL,
Password VARCHAR(100) NOT NULL,
Birthday DATE
);

CREATE TABLE RentalLocations (
LocationID SERIAL PRIMARY KEY,
LocationName VARCHAR(100) NOT NULL,
Address VARCHAR(255) NOT NULL,
City VARCHAR(100) NOT NULL,
State CHAR(2) NOT NULL,
ZipCode VARCHAR(10) NOT NULL,
PhoneNumber VARCHAR(20)
);

CREATE TABLE BikeTypes (
TypeID SERIAL PRIMARY KEY,
TypeName VARCHAR(50) NOT NULL,
Description TEXT
);

CREATE TABLE Trails (
TrailID SERIAL PRIMARY KEY,
Name VARCHAR(100) NOT NULL,
Distance DECIMAL(5,2),
Difficulty VARCHAR(20),
Description TEXT
);

CREATE TABLE Accessories (
AccessoryID SERIAL PRIMARY KEY,
Name VARCHAR(100) NOT NULL,
Price DECIMAL(10,2) NOT NULL,
Description TEXT
);

CREATE TABLE PromoCodes (
PromoCodeID SERIAL PRIMARY KEY,
Code VARCHAR(50) UNIQUE NOT NULL,
Description TEXT,
ExpiryDate DATE,
IsActive BOOLEAN DEFAULT TRUE
);

CREATE TABLE Bikes (
BikeID SERIAL PRIMARY KEY,
TypeID INT NOT NULL REFERENCES BikeTypes(TypeID),
LocationID INT NOT NULL REFERENCES RentalLocations(LocationID),
Size VARCHAR(20),
HourlyRate DECIMAL(10,2) NOT NULL,
Status VARCHAR(20) DEFAULT 'Available'
);

CREATE TABLE Reservations (
ReservationID SERIAL PRIMARY KEY,
UserID INT REFERENCES Users(UserID),
BikeID INT REFERENCES Bikes(BikeID),
TrailID INT REFERENCES Trails(TrailID),
LocationID INT REFERENCES RentalLocations(LocationID),
StartDate TIMESTAMP NOT NULL,
EndDate TIMESTAMP NOT NULL,
TotalCost DECIMAL(10,2),
Status VARCHAR(20) DEFAULT 'Upcoming',
Rating INT CHECK (Rating BETWEEN 1 AND 5),
ReviewText TEXT,
BookingDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Purchases (
PurchaseID SERIAL PRIMARY KEY,
UserID INT REFERENCES Users(UserID),
AccessoryID INT REFERENCES Accessories(AccessoryID),
PurchaseDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
Quantity INT DEFAULT 1,
TotalCost DECIMAL(10,2),
PurchaserName VARCHAR(100),
PurchaserEmail VARCHAR(100),
CONSTRAINT check_purchaser_exists
CHECK (UserID IS NOT NULL OR (PurchaserName IS NOT NULL AND PurchaserEmail IS NOT NULL))
);

-------------------------------------------------------------------------------
-- 2. INSERT DATA (Full Content)
-------------------------------------------------------------------------------

-- 1. Locations (Updated to Indian Creek)
INSERT INTO RentalLocations (LocationName, Address, City, State, ZipCode, PhoneNumber)
VALUES ('Indian Creek Cycle Rentals', '123 Indian Creek Trailhead', 'Overland Park', 'KS', '66210', '913-555-BIKE');

-- 2. Users
INSERT INTO Users (Name, Email, Password, Birthday) VALUES
('Amelia Smith', 'amelia.smith@example.com', 'password123', '1995-01-15'),
('Noah Johnson', 'noah.johnson@example.com', 'password124', '1992-02-20'),
('Olivia Brown', 'olivia.brown@example.com', 'password125', '1988-03-05'),
('Liam Jones', 'liam.jones@example.com', 'password126', '1990-04-12');

-- 3. Bike Types (Full List)
INSERT INTO BikeTypes (TypeName, Description) VALUES
('Balance Bike', 'Lightweight for kids'),
('Childrens Bike', 'Aged 5-12'),
('BMX Bike', 'For tricks'),
('Mountain Bike', 'Off-road adventures'),
('Standard Adult', 'City commuting'),
('Comfort Cruiser', 'Leisurely rides'),
('Hybrid Bike', 'Fitness and commuting'),
('Electric-Assist', 'Battery powered boost'),
('Tandem Bike', 'For two people'),
('Cargo Bike', 'For carrying heavy loads');

-- 4. Bikes (Linked to Indian Creek LocationID 1)
INSERT INTO Bikes (TypeID, LocationID, Size, HourlyRate, Status) VALUES
(1, 1, 'One Size', 15.00, 'Available'),
(2, 1, 'Small', 10.00, 'Available'),
(2, 1, 'Medium', 12.00, 'Rented'),
(3, 1, 'Small', 12.00, 'Available'),
(4, 1, 'Medium', 18.00, 'Available');

-- 5. Trails (Full 20 Locations)
INSERT INTO Trails (Name, Distance, Difficulty, Description) VALUES
('Blue River Trail', 5.0, 'Easy', 'Scenic river views.'),
('Kill Creek Park Trail', 3.5, 'Moderate', 'Wooded areas and open fields.'),
('Shawnee Mission Park Trail', 7.2, 'Moderate', 'Varied terrains.'),
('Indian Creek Trail', 4.8, 'Easy', 'Paved trail.'),
('Mill Creek Streamway Park', 6.0, 'Easy', 'Alongside Mill Creek.'),
('Lenexa Lake Trail', 2.1, 'Easy', 'Loop around the lake.'),
('Heritage Park Trail', 5.5, 'Moderate', 'Beautiful landscapes.'),
('Olathe Lake Trail', 4.0, 'Easy', 'Flat trail.'),
('De Soto Riverfront Park Trail', 3.2, 'Easy', 'Along the Kansas River.'),
('Cedar Creek Trail', 8.0, 'Difficult', 'Steep and rocky.'),
('Prairie Center Trail', 5.5, 'Moderate', 'Prairie and woods.'),
('Riverview Park Trail', 3.0, 'Easy', 'Short river trail.'),
('Weston Bend State Park Trail', 6.8, 'Difficult', 'Rugged river views.'),
('Swope Park Trail', 4.3, 'Moderate', 'Flat and hilly.'),
('Briarwood Trail', 2.8, 'Easy', 'Residential area.'),
('Black Hoof Park Trail', 3.7, 'Easy', 'Family-friendly.'),
('JCCC Trail', 5.0, 'Moderate', 'College campus.'),
('Antioch Park Trail', 4.5, 'Moderate', 'Ponds and wildlife.'),
('Yardley Park Trail', 3.3, 'Easy', 'Flat leisure trail.'),
('Tomahawk Creek Trail', 6.0, 'Moderate', 'Picturesque creek.');

-- 6. Accessories
INSERT INTO Accessories (Name, Price, Description) VALUES
('Helmet', 50.00, 'Safety first!'),
('Water Bottle', 10.00, 'Stay hydrated.'),
('Bike Lock', 25.00, 'Secure your ride.'),
('Bike Bag', 15.00, 'Carry essentials.'),
('Cycling Gloves', 20.00, 'Comfortable grip.'),
('Repair Kit', 12.00, 'Essential tools.'),
('Portable Pump', 22.00, 'For inflating tires.'),
('Reflective Vest', 20.00, 'Visibility and safety.'),
('Saddle Bag', 18.00, 'Storage.'),
('Bike Lights', 15.00, 'LED visibility.');

-- 7. Promo Codes (Full 11 Codes)
INSERT INTO PromoCodes (Code, Description, ExpiryDate, IsActive) VALUES
('SUMMER2026', 'Get 20% off your next bike rental!', '2026-09-01', TRUE),
('FALL2026', '15% discount on rentals for the fall season.', '2026-12-01', TRUE),
('WEEKENDDEAL', 'Rent any bike on the weekend and get 10% off.', '2026-09-30', TRUE),
('FREEHOUR', 'Rent for 2 hours and get the 3rd hour free!', '2026-10-15', TRUE),
('FIRSTRENTAL', '20% off for first-time renters.', '2026-12-31', TRUE),
('GROUPDISCOUNT', 'Rent 3 bikes or more and get 25% off!', '2026-11-15', TRUE),
('MEMBEREXCLUSIVE', 'Exclusive 30% off for members.', '2026-12-31', TRUE),
('HOLIDAYSALE', 'Celebrate the holidays with 15% off all rentals.', '2026-12-25', TRUE),
('WINTER2026', '10% off rentals during the winter months.', '2027-03-01', TRUE),
('REFERAFRIEND', 'Refer a friend and both get 10% off your next rental!', '2026-09-30', TRUE),
('BIRTHDAYFREE', 'Enjoy a free ride for your birthday to use anytime!', '2026-12-31', TRUE);

-- 8. Transaction Samples
INSERT INTO Reservations (UserID, BikeID, TrailID, LocationID, StartDate, EndDate, TotalCost, Status, Rating, ReviewText)
VALUES (1, 1, 1, 1, '2026-03-01 10:00:00', '2026-03-01 12:00:00', 20.00, 'Completed', 5, 'Loved it!');

INSERT INTO Purchases (UserID, AccessoryID, Quantity, TotalCost)
VALUES (1, 1, 1, 50.00);

-------------------------------------------------------------------------------
-- 3. CREATE VIEWS (The Shortcuts)
-------------------------------------------------------------------------------

CREATE OR REPLACE VIEW View_User_Ride_History AS
SELECT u.Name AS Rider, u.Email, t.Name AS Trail_Taken, r.StartDate, r.Status, r.Rating
FROM Reservations r
JOIN Users u ON r.UserID = u.UserID
JOIN Trails t ON r.TrailID = t.TrailID;

CREATE OR REPLACE VIEW View_Admin_Sales_Summary AS
SELECT 'Rental' AS Category, TotalCost, BookingDate AS Transaction_Date FROM Reservations
UNION ALL
SELECT 'Accessory' AS Category, TotalCost, PurchaseDate AS Transaction_Date FROM Purchases;

CREATE OR REPLACE VIEW View_Bike_Status_Report AS
SELECT b.BikeID, bt.TypeName, b.Size, b.Status, rl.LocationName AS Current_Home
FROM Bikes b
JOIN BikeTypes bt ON b.TypeID = bt.TypeID
JOIN RentalLocations rl ON b.LocationID = rl.LocationID;

CREATE OR REPLACE VIEW View_Available_Inventory AS
SELECT
b.BikeID AS Reference_Number,
bt.TypeName AS Bicycle_Type,
b.Size,
b.HourlyRate
FROM Bikes b
JOIN BikeTypes bt ON b.TypeID = bt.TypeID
WHERE b.Status = 'Available';

