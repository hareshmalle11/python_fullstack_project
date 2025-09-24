# Parking management

This project is a Vehicle Parking Management System. It automates the tracking of vehicles entering and exiting a parking facility, managing the allocation of parking slots, and calculating parking fees based on vehicle type and duration. The system uses a database to maintain real-time records of slot occupancy and a history of all parking transactions

# features

1)Add Parking Slots (slot number, type: 2-wheeler/4-wheeler).

2)Check Availability (see free/occupied slots).

3)Allocate Slot (assign a slot to a vehicle).

4)Release Slot (when vehicle leaves).

5)Track Vehicle Details (vehicle number, entry/exit time).

6)Generate Report (daily usage, income if you add charges).

# Project Structure

 Parking_management/
 |
 |---src            # Core-applictaion logic
 |   |___logic.py   # BUsiness logic and task
 |   |___db.py      # Database Operations
 |
 |---api/           # Backend API  
 |   |___main.py    # FastAPI endpoints
 |
 |---frontend/      # Frontend Applications
 |   |___app.py     # Streamlit web interface
 |
 |___requirements.txt   # python dependencies
 |
 |___README.md      # Project Documentation
 |
 |___.env           # Python Variables

 # Quick Start

 ## Prerequisites
  -python 3.8 or higher 
  -A superbase account
  -Git(push,cloning)
  

 ## 1.clone or Downloading the Project
   # Option 1 : Clone with git
    -git clone <repository url>
   # Option 2:Download or Extract the ZIP file

 ## 2.Install the Dependencies
  -pip install -r requirements.txt

 ## 3.Set up Supabase Databse
  1.create a superbase project:
  2.create a task table:
     -go to the SQL Editor in your Supabase dashboard
     -Run the SQL command:
         '''sql
         CREATE TABLE vehicle_types (
             type_id SERIAL PRIMARY KEY,
             type_name VARCHAR(10) UNIQUE NOT NULL,
             total_slots INT NOT NULL,
             cost_per_hour DECIMAL(10,2) NOT NULL
            );'''
  