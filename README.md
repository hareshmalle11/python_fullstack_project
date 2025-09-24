# Parking Management

This project is a Vehicle Parking Management System. It automates the tracking of vehicles entering and exiting a parking facility, managing the allocation of parking slots, and calculating parking fees based on vehicle type and duration. The system uses a Supabase database to maintain real-time records of slot occupancy and a history of all parking transactions

# features

* Add Parking Slots (slot number, type: 2-wheeler/4-wheeler).
* Check Availability (see free/occupied slots).
* Allocate Slot (assign a slot to a vehicle).
* Release Slot (when vehicle leaves).
* Track Vehicle Details (vehicle number, entry/exit time).
* Generate Report (daily usage, income if you add charges).

# Project Structure

```
Parking_management/
|
|---src            # Core-applictaion logic
|   |---logic.py   # BUsiness logic and task
|   |---db.py      # Database Operations
|
|---api/           # Backend API  
|   |---main.py    # FastAPI endpoints
|
|---frontend/      # Frontend Applications
|   |---app.py     # Streamlit web interface
|
|---requirements.txt   # python dependencies
|
|---README.md      # Project Documentation
|
|---.env           # Python Variables
```

# Quick Start

## Prerequisites
* python 3.8 or higher 
* A superbase account
* Git(push,cloning)

## 1.clone or Downloading the Project
* Option 1 : Clone with git
  - git clone <repository url>
* Option 2:Download or Extract the ZIP file

## 2.Install the Dependencies
* pip install -r requirements.txt

## 3.Set up Supabase Databse
* create a superbase project
* create a task table
  - go to the SQL Editor in your Supabase dashboard
  - Run the SQL command:
    ```sql
    CREATE TABLE vehicle_types (
        type_id SERIAL PRIMARY KEY,
        type_name VARCHAR(10) UNIQUE NOT NULL,
        total_slots INT NOT NULL,
        cost_per_hour DECIMAL(8,2) NOT NULL
    );
    ```
* get your credentials

## 4.Configure Environment vaiables
* Create .env file in the project root
* add your Supabse credentials to .env :
  - SUPABASE_URL=your_url
  - SUPABASE_KEY=your_key

## 5.Run the Application
* Streamlit Frontend
  - streamlit run frontend/app.py
  - this will be open in your browser at http://loacalhost:8501
* FastAPI
  - cd api
  - python main.py
  - the api will be available at http://localhost:8000

# How to Use
* Access the Streamlit frontend
  - Open http://localhost:8501 in your browser
  - Add new parking slots
  - Check slot availability
  - Allocate or release slots
  - Enter vehicle details (vehicle number, type)
  - Generate daily usage and income reports
* Interact with FastAPI backend
  - Use tools like Postman to access http://localhost:8000
  - Example endpoints:
    - GET /slots: View slot availability
    - POST /allocate: Assign a slot to a vehicle
    - POST /release: Free a slot

# Technical Details

## Technologies used
* *Frontend* : Streamlit (Python web framework)
* *Backend* : FastAPI (Python REST API framework)
* *Database* : supabase (postgreSQL-based backend -as-a-service)
* *Language* : Python 3.8+

## Key Components
* *src/db.py* : Database operations
  - Handles all CRUD operations with supabase
* *src/logic.py* : Business logic
  - Task validation and processing
* *api/main.py* : FastAPI endpoints
  - Defines API routes for programmatic access
* *frontend/app.py* : Streamlit interface
  - User-friendly web interface

# Troubleshooting

## common Issues
* Supabase connection errors
  - *Problem*: Invalid Supabase URL or Key
  - *Solution*: Verify SUPABASE_URL and SUPABASE_KEY in .env match your Supabase credentials
* Dependency installation fails
  - *Problem*: Errors during pip install
  - *Solution*: Ensure Python 3.8+ is installed, upgrade pip with `pip install --upgrade pip`
* Application not running
  - *Problem*: Streamlit or FastAPI fails to start
  - *Solution*: Check if ports 8501 (Streamlit) or 8000 (FastAPI) are in use using `lsof -i :8501` or `lsof -i :8000`
* Database table not found
  - *Problem*: Missing vehicle_types table
  - *Solution*: Ensure the SQL command in Step 3 was executed

# Future Enhancements
* Intuitive dashboard: Create a user-friendly admin dashboard for managing slots, vehicles, and reports easily. Use clear visualizations and filtering options.
* Mobile-first design: Optimize the user interface for mobile devices. Users should be able to view availability, reserve a spot, and pay from their smartphones.
* Interactive lot map: Display a real-time, color-coded map of the parking lot showing available and occupied spots. This could also guide drivers to an open space.
* Electric Vehicle (EV) charging: Add EV charging stations to your parking facility
* License Plate Recognition (LPR): Use cameras and computer vision to automatically read license plates upon entry and exit

# Support
* If you encounter any issues or have questions:
  - mail id  : [Insert email address]
  - phone no : +91 85558 28332