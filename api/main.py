from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.db import DatabaseManager
from src.logic import ParkingLogic, AdminManager

# App setup
app = FastAPI(title="Parking Management System", version="1.0")

# Allow frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize parking logic
db_manager = DatabaseManager()
admin_manager = AdminManager(db_manager.supabase)
parking_logic = ParkingLogic(db_manager, admin_manager)

# Data models
class ParkRequest(BaseModel):
    name: str
    vehicle_number: str
    type_id: int

class UnparkRequest(BaseModel):
    vehicle_number: str

class UpdateSlotsRequest(BaseModel):
    type_id: int
    new_slots: int

class FreeSlotsRequest(BaseModel):
    type_id: int

class ParkingIDStatusRequest(BaseModel):
    type_id: int

class LoginRequest(BaseModel):
    username: str
    password: str

class VehicleTypeRequest(BaseModel):
    type_name: str
    total_slots: int
    cost_per_hour: float

class UpdateCostRequest(BaseModel):
    type_id: int
    new_cost: float

class UpdateTypeNameRequest(BaseModel):
    type_id: int
    new_name: str

class RestrictedVehicleRequest(BaseModel):
    vehicle_number: str




#new block
class VehicleRecordsRequest(BaseModel):
    vehicle_number: str


class VehiclesByDateRangeRequest(BaseModel):
    start_date: str
    end_date: str
    type_id: Optional[int] = None


class VehiclesBySpecificDateRequest(BaseModel):
    specific_date: str
    type_id: Optional[int] = None


#end of new block


# API endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the Parking Management System API"}

@app.post("/login")
def login_admin(request: LoginRequest):
    result = parking_logic.login_admin(request.username, request.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])
    return result

@app.post("/logout")
def logout_admin():
    return parking_logic.logout_admin()

@app.post("/add_vehicle_type")
def add_vehicle_type(request: VehicleTypeRequest):
    result = parking_logic.add_vehicle_type(request.type_name, request.total_slots, request.cost_per_hour)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
@app.post("/update_slots")
def update_slots(request: UpdateSlotsRequest):
    result = parking_logic.update_vehicle_slots(request.type_id, request.new_slots)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/remove_vehicle_type/{type_id}")
def remove_vehicle_type(type_id: int):
    result = parking_logic.remove_vehicle_type(type_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.put("/update_cost")
def update_vehicle_cost(request: UpdateCostRequest):
    result = parking_logic.update_vehicle_cost(request.type_id, request.new_cost)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.put("/update_type_name")
def update_vehicle_type_name(request: UpdateTypeNameRequest):
    result = parking_logic.update_vehicle_type_name(request.type_id, request.new_name)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/add_restricted_vehicle")
def add_restricted_vehicle(request: RestrictedVehicleRequest):
    result = parking_logic.add_restricted_vehicle(request.vehicle_number)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/remove_restricted_vehicle/{vehicle_number}")
def remove_restricted_vehicle(vehicle_number: str):
    result = parking_logic.remove_restricted_vehicle(vehicle_number)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/status")
def get_status():
    return parking_logic.get_parking_status()

@app.post("/park")
def park_vehicle(request: ParkRequest):
    result = parking_logic.park_vehicle(request.name, request.vehicle_number, request.type_id)
    if isinstance(result, str) and "Hello" in result:
        return {"message": result}
    elif isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/unpark")
def unpark_vehicle(request: UnparkRequest):
    result = parking_logic.unpark_vehicle(request.vehicle_number)
    if isinstance(result, str):
        return {"message": result}
    elif isinstance(result, dict):
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.put("/update_slots")
def update_slots(request: UpdateSlotsRequest):
    result = parking_logic.update_vehicle_slots(request.type_id, request.new_slots)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/free_slots")
def get_free_slots(request: FreeSlotsRequest):
    result = parking_logic.get_free_slots(request.type_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/parking_id_status")
def get_parking_id_status(request: ParkingIDStatusRequest):
    result = parking_logic.get_parking_id_status(request.type_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result



#new block
@app.post("/vehicle_records")
def get_vehicle_records(request: VehicleRecordsRequest):
    """Fetch all parking records for a given vehicle number."""
    result = parking_logic.get_vehicle_records(request.vehicle_number)
    return result if not (isinstance(result, dict) and "message" in result) else result


@app.post("/vehicles_by_date_range")
def get_vehicles_by_date_range(request: VehiclesByDateRangeRequest):
    """Fetch all vehicles (parked or unparked) between two given dates."""
    result = parking_logic.get_vehicles_by_date_range(
        request.start_date, request.end_date, request.type_id
    )
    return result if not (isinstance(result, dict) and "message" in result) else result


@app.post("/vehicles_by_specific_date")
def get_vehicles_by_specific_date(request: VehiclesBySpecificDateRequest):
    """Fetch all vehicles (parked or unparked) for a specific date."""
    result = parking_logic.get_vehicles_by_specific_date(
        request.specific_date, request.type_id
    )
    return result if not (isinstance(result, dict) and "message" in result) else result
#end of new block



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)