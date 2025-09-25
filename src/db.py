import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime


#loading Enviriment Variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")


supabase=create_client(url, key)

#create task
def get_vehicle_types():
    response = supabase.table("vehicle_types").select("*").execute()
    return response.data

def update_vehicle_slots(type_id: int, new_total: int):
    type_res = supabase.table("vehicle_types").select("*").eq("type_id", type_id).single().execute()
    vehicle_type = type_res.data
    if not vehicle_type:
        return {"error": "Vehicle type not found"}
    current_total = vehicle_type["total_slots"]
    # If new total is same → nothing to do
    if new_total == current_total:
        return {"message": "No change in slots"}
    # Update vehicle_types table
    supabase.table("vehicle_types").update({"total_slots": new_total}).eq("type_id", type_id).execute()
    # If increasing → add free slots
    if new_total > current_total:
        diff = new_total - current_total
        new_slots = [{"type_id": type_id, "is_occupied": False} for _ in range(diff)]
        supabase.table("parking_slots").insert(new_slots).execute()
        return {"message": f"Added {diff} new slots", "new_total": new_total}
    # If decreasing → remove free slots only
    elif new_total < current_total:
        diff = current_total - new_total
        # Get free slots to delete
        free_slots_res = (
            supabase.table("parking_slots")
            .select("slot_id")
            .eq("type_id", type_id)
            .eq("is_occupied", False)
            .limit(diff)
            .execute()
        )
        free_slots = [slot["slot_id"] for slot in free_slots_res.data]
        if len(free_slots) < diff:
            return {"error": "Not enough free slots to reduce — occupied slots prevent deletion"}
        # Delete selected free slots
        for sid in free_slots:
            supabase.table("parking_slots").delete().eq("slot_id", sid).execute()
        return {"message": f"Removed {diff} slots", "new_total": new_total}



def get_free_slots(type_id: int):
    """Return free slots for given vehicle type (temporary debug version)."""
    response = (
        supabase.table("parking_slots")
        .select("*")  # Fetch rows instead of count
        .eq("type_id", type_id)
        .eq("is_occupied", False)  # Limit for safety
        .execute()
    )
    return len(response.data)  # Return count of fetched rows

def allocate_slot(vehicle_number: str, type_id: int):
    """Allocate first free slot to a vehicle and create parking record."""
    # Check if vehicle is already parked (out_time IS NULL)
    existing_record = (
        supabase.table("parking_records")
        .select("*")
        .eq("vehicle_number", vehicle_number)
        .is_("out_time", "null")
        .execute()
    )
    if existing_record.data:
        return {"error": f"Vehicle {vehicle_number} is already parked"}

    # Check free slots
    if get_free_slots(type_id) == 0:
        return {"error": "No free slots available"}

    # Get first free slot
    free_slot_res = (
        supabase.table("parking_slots")
        .select("*")
        .eq("type_id", type_id)
        .eq("is_occupied", False)
        .limit(1)
        .execute()
    )
    if not free_slot_res.data:
        return {"error": "No free slots available"}

    slot_id = free_slot_res.data[0]["slot_id"]

    # Mark slot as occupied
    supabase.table("parking_slots").update({"is_occupied": True}).eq("slot_id", slot_id).execute()

    # Create parking record
    record = {
        "vehicle_number": vehicle_number,
        "type_id": type_id,
        "slot_id": slot_id,
        "in_time": datetime.now().isoformat()
    }
    response = supabase.table("parking_records").insert(record).execute()
    return response.data[0]


def release_slot(record_id: int):
    """Release slot when vehicle exits and calculate cost."""
    # Get record
    record_res = supabase.table("parking_records").select("*").eq("record_id", record_id).single().execute()
    record = record_res.data
    if not record:
        return {"error": "Record not found"}

    slot_id = record["slot_id"]
    type_id = record["type_id"]

    # Fetch cost per hour
    type_res = supabase.table("vehicle_types").select("cost_per_hour").eq("type_id", type_id).single().execute()
    cost_per_hour = float(type_res.data["cost_per_hour"])

    # Calculate cost
    in_time = datetime.fromisoformat(record["in_time"])
    out_time = datetime.now()
    hours = max(1, int((out_time - in_time).total_seconds() // 3600))  # Round down, min 1 hour
    total_cost = hours * cost_per_hour

    # Update record with out_time + cost
    supabase.table("parking_records").update({
        "out_time": out_time.isoformat(),
        "cost": total_cost
    }).eq("record_id", record_id).execute()

    # Free the slot
    supabase.table("parking_slots").update({"is_occupied": False}).eq("slot_id", slot_id).execute()

    return {"record_id": record_id, "cost": total_cost, "hours": hours}

def get_status_report():
    """Return count of occupied and free slots for each vehicle type."""
    report = {}

    # Get all types
    types = get_vehicle_types()
    for t in types:
        type_id = t["type_id"]
        type_name = t["type_name"]
        total = t["total_slots"]

        # Count occupied
        occ_res = (
            supabase.table("parking_slots")
            .select("*", count="exact")  # Use count="exact" instead of count(*)
            .eq("type_id", type_id)
            .eq("is_occupied", True)
            .execute()
        )
        occupied = occ_res.count  # Get count from response metadata
        free = total - occupied

        report[type_name] = {"total": total, "occupied": occupied, "free": free}

    return report
#print(get_vehicle_types())
#print(get_status_report())
#print(get_free_slots(1))
#print(allocate_slot("ABC123", 1))
#print(release_slot(1))