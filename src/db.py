import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

# Load environment variables (.env)
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug environment variables
#print(f"SUPABASE_URL: {SUPABASE_URL}")
#print(f"SUPABASE_KEY: {SUPABASE_KEY[:10]}...")  # Partial key for safety
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing in .env file")

class DatabaseManager:
    def __init__(self):
        """Initialize Supabase client."""
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_vehicle_types(self):
        """Fetch all vehicle types with capacity and cost."""
        response = self.supabase.table("vehicle_types").select("*").execute()
        return response.data


    


    #admin section
    def update_vehicle_slots(self, type_id: int, new_total: int):
        type_res = self.supabase.table("vehicle_types").select("total_slots").eq("type_id", type_id).execute()
        if not type_res.data:
            return {"error": "Vehicle type not found"}
        
        current_total_slots = type_res.data[0]["total_slots"]
        parked_res = self.supabase.table("parking_slots").select("parked").eq("type_id", type_id).single().execute()
        
        current_parked_count = parked_res.data["parked"] if parked_res.data else 0

        if new_total < 0:
            return {"error": "New total slots cannot be negative."}
        if new_total < current_parked_count:
            return {"error": f"Cannot decrease total slots to {new_total}. There are currently {current_parked_count} vehicles parked."}
        if new_total == current_total_slots:
            return {"message": "No change in slots needed."}

        self.supabase.table("vehicle_types").update({"total_slots": new_total}).eq("type_id", type_id).execute()

        if new_total > current_total_slots:
            slots_added = new_total - current_total_slots
            return {"message": f"Added {slots_added} new slots. New total: {new_total}"}
        else:
            slots_removed = current_total_slots - new_total
            return {"message": f"Removed {slots_removed} slots. New total: {new_total}"}

    def admin_add_vehicle_type(self, type_id:int,type_name: str, total_slots: int, cost_per_hour: float):
        vehicle_type_data = {
            "type_id": type_id,
            "type_name": type_name,
            "total_slots": total_slots,
            "cost_per_hour": cost_per_hour
        }
        response = self.supabase.table("vehicle_types").insert(vehicle_type_data).execute()
        if response.data:
            new_type_id = response.data[0]['type_id']
            self.supabase.table("parking_slots").insert({"type_id": new_type_id, "parked": 0}).execute()
            return response.data[0]
        return {"error": "Failed to add vehicle type."}

    def admin_remove_vehicle_type(self, type_id: int):
        try:
            parked_res = self.supabase.table("parking_slots").select("parked").eq("type_id", type_id).single().execute()
            parked_count = parked_res.data["parked"] if parked_res.data else 0
            
            if parked_count > 0:
                return {"error": f"Cannot remove vehicle type {type_id}. There are currently {parked_count} vehicles parked."}

            self.supabase.table("parking_records").delete().eq("type_id", type_id).execute()

            self.supabase.table("vehicle_types").delete().eq("type_id", type_id).execute()
            
            return {"message": f"Vehicle type {type_id} removed successfully."}
    
        except Exception as e:
            return {"error": f"Failed to remove vehicle type: {e}"}

    def admin_update_cost(self, type_id: int, new_cost: float):
        response = self.supabase.table("vehicle_types").update({"cost_per_hour": new_cost}).eq("type_id", type_id).execute()
        if response.data:
            return {"message": "Cost updated successfully."}
        return {"error": "Failed to update cost."}

    def admin_update_type_name(self, type_id: int, new_name: str):
        response = self.supabase.table("vehicle_types").update({"type_name": new_name}).eq("type_id", type_id).execute()
        if response.data:
            return {"message": "Vehicle type name updated successfully."}
        return {"error": "Failed to update vehicle type name."}

    def admin_add_restricted_vehicle(self, vehicle_number: str):
        try:
            self.supabase.table("restricted_vehicles").insert({"vehicle_number": vehicle_number}).execute()
            return {"message": f"Vehicle {vehicle_number} added to restricted list."}
        except APIError as e:
            return {"error": "Failed to add restricted vehicle. It may already exist."}

    def admin_remove_restricted_vehicle(self, vehicle_number: str):
        self.supabase.table("restricted_vehicles").delete().eq("vehicle_number", vehicle_number).execute()
        return {"message": f"Vehicle {vehicle_number} removed from restricted list."}








    def get_free_slots(self, type_id: int):
        total_slots_res = self.supabase.table("vehicle_types").select("total_slots").eq("type_id", type_id).execute()
        
        if not total_slots_res.data:
            return {"error": "Vehicle type not found"}
        
        total_slots = total_slots_res.data[0]["total_slots"]

        parked_count_res = self.supabase.table("parking_slots").select("parked").eq("type_id", type_id).single().execute()
        
        parked_count = parked_count_res.data["parked"] if parked_count_res.data else 0

        free_slots = total_slots - parked_count
        return {"free_slots": free_slots}

    def allocate_slot(self, name: str, vehicle_number: str, type_id: int):
            """Allocate a parking slot for a vehicle."""
            restricted_res = self.supabase.table("restricted_vehicles").select("vehicle_number").eq("vehicle_number", vehicle_number).execute()
            if restricted_res.data:
                return {"error": f"Vehicle {vehicle_number} is not allowed to park."}
            # Check if vehicle is already parked
            existing_record = (
                self.supabase.table("parking_records")
                .select("*")
                .eq("vehicle_number", vehicle_number)
                .is_("out_time", "null")
                .execute()
            )
            if existing_record.data:
                return {"error": f"Vehicle {vehicle_number} is already parked"}

            # Check available slots
            free_slots = self.get_free_slots(type_id)

            if free_slots["free_slots"] <= 0:
                return {"error": "No free slots available"}

            # Increment parked count
            parked_res = self.supabase.table("parking_slots").select("parked").eq("type_id", type_id).single().execute()


            # Create parking record
            record = {
                "name": name,
                "type_id": type_id,
                "vehicle_number": vehicle_number,
                "in_time": datetime.now().isoformat()
            }
            response = self.supabase.table("parking_records").insert(record).execute()
            new_parked_count = parked_res.data["parked"] + 1 if parked_res.data else 1
            self.supabase.table("parking_slots").update({"parked": new_parked_count}).eq("type_id", type_id).execute()
            return f"Hello {name}! Your vehicle {response.data[0]['vehicle_number']} is parked with parking ID: {response.data[0]['record_id']}"

    def release_slot(self, record_id: int):
        """Release a parking slot and calculate cost."""
        # Fetch parking record
        record_res = self.supabase.table("parking_records").select("*").eq("record_id", record_id).single().execute()
        if not record_res.data:
            return {"error": "Record not found"}
        record = record_res.data


        type_id = record["type_id"]
        
        # Fetch cost per hour
        type_res = self.supabase.table("vehicle_types").select("cost_per_hour").eq("type_id", type_id).single().execute()
        if not type_res.data:
            return {"error": "Vehicle type not found"}
        cost_per_hour = float(type_res.data["cost_per_hour"])

        # Calculate parking duration and cost
        in_time = datetime.fromisoformat(record["in_time"])
        out_time = datetime.now()
        hours = max(1, (out_time - in_time).total_seconds() / 3600)  # Minimum 1 hour
        total_cost = round(hours * cost_per_hour, 2)

        # Update parking record
        self.supabase.table("parking_records").update({
            "out_time": out_time.isoformat(),
            "cost": total_cost
        }).eq("record_id", record_id).execute()

        # Decrement parked count
        parked_res = self.supabase.table("parking_slots").select("parked").eq("type_id", type_id).single().execute()
        if parked_res.data:
            new_parked_count = max(0, parked_res.data["parked"] - 1)
            self.supabase.table("parking_slots").update({"parked": new_parked_count}).eq("type_id", type_id).execute()
        return f"Thank you {record["name"]}! Vehicle {record['vehicle_number']} unparked. Total cost: ₹{total_cost}"

    def get_status_report(self):
            """Return count of occupied and free slots for each vehicle type."""
            report = {}
            types = self.get_vehicle_types()
            for t in types:
                type_id = t["type_id"]
                type_name = t["type_name"]
                total = t["total_slots"]
                free_slots = self.get_free_slots(type_id)

                occupied = total - free_slots["free_slots"]
                report[type_id] = {
                    "vehicle": type_name,
                    "total": total,
                    "occupied": occupied,
                    "free": free_slots["free_slots"]
                }
            return report
        
    def get_parking_id_report(self, type_id: int):
            """Return all parked vehicles (not yet unparked) of a particular type."""
            records = (
                self.supabase.table("parking_records")
                .select("*")
                .eq("type_id", type_id)
                .is_("out_time", "null")
                .execute()
            )
            return records.data if records.data else {"message": "No vehicles currently parked of this type"}
a=DatabaseManager()
#print(a.get_free_slots(1))
#print(a.update_vehicle_slots(3,10)) 
#print(a.allocate_slot("gokul","KA-03-HH-1234",2))
#print(a.release_slot(1))
#print(a.get_status_report())
#print(a.get_parking_id_report(1))
        
        