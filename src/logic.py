from src.db import DatabaseManager
from datetime import datetime
import bcrypt
from supabase import Client

class AdminManager:
    def __init__(self, supabase: Client):
        self.supabase = supabase

    '''def create_admin(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        response = self.supabase.table("admins").insert({
            "username": username,
            "password_hash": hashed_password
        }).execute()
        return response'''
    def authenticate_admin(self, username, password):
        try:
            response = self.supabase.table("admins").select("password_hash").eq("username", username).execute()
            #print(response)

            if not response.data:
                return False

            stored_password = response.data[0]["password_hash"]
            return stored_password == password
        except Exception:
            return False
class ParkingLogic:
    def __init__(self, db_manager, admin_manager):
        self.db_manager = db_manager
        self.admin_manager = admin_manager
        self.is_admin_logged_in = False

    # --- Admin Session Methods ---
    def login_admin(self, username, password):
        if self.admin_manager.authenticate_admin(username, password):
            self.is_admin_logged_in = True
            #print("Admin logged in successfully.")
            return {"message": "Login successful. Admin access granted."}
        else:
            return {"error": "Authentication failed. Invalid username or password."}
    
    def logout_admin(self):
        self.is_admin_logged_in = False
        return {"message": "Logged out successfully."}
    
    # --- Admin Methods (Now simplified to check session status) ---
    def _check_admin_session(self):
        if not self.is_admin_logged_in:
            return {"error": "Access denied. Please log in first."}
        return None

    def add_vehicle_type(self, type_name: str, total_slots: int, cost_per_hour: float):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_add_vehicle_type(type_name, total_slots, cost_per_hour)

    def remove_vehicle_type(self, type_id: int):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_remove_vehicle_type(type_id)

    def update_vehicle_cost(self, type_id: int, new_cost: float):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_update_cost(type_id, new_cost)

    def update_vehicle_slots(self, type_id: int, new_total: int):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.update_vehicle_slots(type_id, new_total)

    def update_vehicle_type_name(self, type_id: int, new_name: str):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_update_type_name(type_id, new_name)

    def add_restricted_vehicle(self, vehicle_number: str):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_add_restricted_vehicle(vehicle_number)

    def remove_restricted_vehicle(self, vehicle_number: str):
        error = self._check_admin_session()
        if error: return error
        return self.db_manager.admin_remove_restricted_vehicle(vehicle_number)

    def park_vehicle(self, name:str,vehicle_number: str, type_id: int):
        result= self.db_manager.allocate_slot(name,vehicle_number, type_id)
        if result:
            return result
        else:
            return "No available slots."

    def unpark_vehicle(self, parking_id: int):
        """Release slot and calculate parking cost."""
        result = self.db_manager.release_slot(parking_id)
        if result:
            return result
            
        else:
            return "❌ Invalid parking ID or vehicle already unparked."

    def get_parking_status(self):
        return self.db_manager.get_status_report()
    

    def get_parking_id_status(self, type_id: int):
        return self.db_manager.get_parking_id_report(type_id)
    

    def get_free_slots(self, type_id: int):
        free = self.db_manager.get_free_slots(type_id)
        #return f"Free slots available for type {type_id}: {free["free_slots"]}"
        return free
    

    def update_vehicle_slots(self, type_id: int, new_slots: int):
        """
        Update number of slots for a vehicle type.
        Ensures no overflow and keeps parking slots in sync.
        """
        updated = self.db_manager.update_vehicle_slots(type_id, new_slots)
        if updated:
            return updated
        else:
            return "❌ Failed to update slots (check limits or constraints)."
db_manager_instance = DatabaseManager()
b=AdminManager(db_manager_instance.supabase)
a=ParkingLogic(db_manager_instance,b)
#b.authenticate_admin("hareshmalle11","Haresh@123")
#print(a.login_admin("hareshmalle11","Haresh@123"))
#print(a.update_vehicle_cost(2,17.0))


#print(a.get_free_slots(1))

#print(a.park_vehicle("hari","KA-01-HH-1034",1))
    
    
