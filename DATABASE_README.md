Indian Creek Cycle Rentals & Gear
  Location: 123 Indian Creek trailhead Overland Park, KS 66210 (913) 555-BIKE

Website Content Guide
  Front-end & Admin developers: Use data below to populate the website pages. This matches
  the data stored in the setup_database.sql script.
  
1. Rental Fleet & Pricing
  - Bike Type Sizes & Rates
  - Balance Bike One Size: $15.00/hr
  - Children's Bike Small: $10.00, Medium: $12.00
  - BMX Bike Small: $12.00, Medium: $14.00
  - Mountain Bike Small: $15.00, Medium: $18.00
  - Standard Adult Small: $12.00, Medium: $15.00, Large: $18.00
  - Comfort Cruiser Small: $10.00, Medium: $12.00, Large: $15.00
  - Hybrid/Fitness Small: $12.00, Medium: $15.00, Large: $18.00
  - Electric-Assist Small: $15.00, Medium: $18.00, Large: $20.00
  - Tandem Bike One Size: $20.00/hr
  - Cargo Bike One Size: $25.00/hr

2. Trail Gallery (20 Locations)
  - Blue River Trail: 5.0 miles | Easy | Scenic river views.
  - Kill Creek Park Trail: 3.5 miles | Moderate | Wooded areas and open fields.
  - Shawnee Mission Park: 7.2 miles | Moderate | Varied terrains and beautiful views.
  - Indian Creek Trail: 4.8 miles | Easy | Paved trail for casual strolls.
  - Mill Creek Streamway: 6.0 miles | Easy | Runs alongside Mill Creek.
  - Lenexa Lake Trail: 2.1 miles | Easy | Short loop around the lake.
  - Heritage Park Trail: 5.5 miles | Moderate | Beautiful landscapes and picnic spots.
  - Olathe Lake Trail: 4.0 miles | Easy | Flat trail for running and biking.
  - De Soto Riverfront: 3.2 miles | Easy | Peaceful trail along the Kansas River.
  - Cedar Creek Trail: 8.0 miles | Difficult | Steep inclines and rocky paths.
  - Prairie Center Trail: 5.5 miles | Moderate | Mix of open prairie and wooded areas.
  - Riverview Park Trail: 3.0 miles | Easy | Short, easy trail along the river.
  - Weston Bend State Park: 6.8 miles | Difficult | Rugged trail with stunning river views.
  - Swope Park Trail: 4.3 miles | Moderate | Diverse flat and hilly sections.
  - Briarwood Trail: 2.8 miles | Easy | Quaint trail through residential areas.
  - Black Hoof Park: 3.7 miles | Easy | Family-friendly with playgrounds.
  - JCCC Trail: 5.0 miles | Moderate | Runs through the college campus.
  - Antioch Park Trail: 4.5 miles | Moderate | Ponds and wildlife.
  - Yardley Park Trail: 3.3 miles | Easy | Short and flat for families.
  - Tomahawk Creek Trail: 6.0 miles | Moderate | Picturesque wildlife opportunities.

3. Active Promotions
  - SUMMER2026: 20% off rentals.
  - FALL2026: 15% off rentals.
  - WEEKENDDEAL: 10% off any weekend ride.
  - FREEHOUR: Rent 2 hours, get the 3rd free.
  - FIRSTRENTAL: 20% off for new members.
  - GROUPDISCOUNT: 25% off for 3+ bikes.
  - MEMBEREXCLUSIVE: 30% off for registered users.
  - BIRTHDAYFREE: One free ride for birthdays.
  - REFERAFRIEND: 10% off for both parties.

4. Accessories Shop
    Helmet: $50.00 | Water Bottle: $10.00 | Bike Lock: $25.00
    Bike Bag: $15.00 | Cycling Gloves: $20.00 | Repair Kit: $12.00
    Portable Pump: $22.00 | Reflective Vest: $20.00 | Saddle Bag: $18.00
    Bike Lights: $15.00

Developer Database Access
  Treat these Views as virtual tables to simplify your code and avoid complex JOINs.
  - User Activity & History: SELECT * FROM View_User_Ride_History;
  - Admin Sales Summary: SELECT * FROM View_Admin_Sales_Summary;
  - Real-Time Inventory Status: SELECT * FROM View_Bike_Status_Report;
  - SELECT * FROM View_Available_Inventory;

Data Integrity Features
  1. Automated Validation: The Purchases table features a built-in guardrail
  (check_purchaser_exists).
  2. Transaction Rules: To log a purchase, the system requires either a UserID (registered
  member) OR a PurchaserName and PurchaserEmail (guest). This ensures we never
  have "anonymous" sales data.
  3. Smart Naming: Use the views above to automatically see unified customer names, even
  if they checked out as a guest.

Technical Quick-Start
  1. Run the CREATE TABLE section of the script first.
  2. Run the INSERT data section to populate the fleet, trails, and shop.
  3. Run the CREATE VIEW section last to enable the developer shortcuts.