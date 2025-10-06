import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
API_URL = "https://park-backend-5vgz.onrender.com"

# Inject custom CSS
st.markdown("""
    <style>
        button.step-up {display: none;}
        button.step-down {display: none;}
        .stApp {
            background-color: black;
            font-family: 'Arial', sans-serif;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stTextInput > div > div > input, .stNumberInput > div > div > input {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
        }
        h1 {
            color: #333333;
            text-align: center;
            padding: 20px;
        }
        .admin-container {
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 1000;
            width: 250px;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSelectbox > div > div > select {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 10px;
            width: 100%;
        }
        .stTextInput > div > div > input {
            width: 100%;
        }
        .stForm {
            margin-bottom: 10px;
        }
        .hidden {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Parking Management System")

# Session state for admin login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# Home page content
st.write("Welcome to the Parking Management System. Please use the admin login to manage the system.")

# Admin section in top-right corner
with st.container():
    st.markdown('<div class="admin-container">', unsafe_allow_html=True)
    if not st.session_state.admin_logged_in:
        if not st.session_state.show_login:
            if st.button("Admin Login", key="login_toggle"):
                st.session_state.show_login = True
        if st.session_state.show_login:
            with st.form(key="login_form"):
                st.markdown("**Admin Login**")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Login")
                if submit_login:
                    if username and password:
                        try:
                            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                            result = response.json()
                            if response.status_code == 200 and "message" in result:
                                st.session_state.admin_logged_in = True
                                st.session_state.show_login = False
                                st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>{result.get('detail', 'Authentication failed')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>Please enter both username and password.</p>", unsafe_allow_html=True)
                if st.session_state.get("login_cancel", False):
                    st.session_state.show_login = False
    else:
        st.write("Admin logged in")  # Debug to confirm state
        admin_option = st.selectbox(
        "Admin Actions",
        ["Select Action", "Update Parking Slots","Add Vehicle Type", "Update Vehicle Cost", "Add Restricted Vehicle", "Remove Restricted Vehicle"],
        key="admin_dropdown"
        )
        if admin_option == "Add Vehicle Type":
            with st.form(key="add_vehicle_form"):
                type_name = st.text_input("Vehicle Type Name")
                total_slots = st.number_input("Total Slots", min_value=0, step=1, format="%d")
                cost_per_hour = st.number_input("Cost per Hour", min_value=0.0, step=0.01)
                submit_add_vehicle = st.form_submit_button("Add Vehicle Type")
                if submit_add_vehicle:
                    if type_name and total_slots >= 0 and cost_per_hour >= 0:
                        try:
                            response = requests.post(f"{API_URL}/add_vehicle_type", json={
                                "type_name": type_name,
                                "total_slots": total_slots,
                                "cost_per_hour": cost_per_hour
                            })
                            result = response.json()
                            if response.status_code == 200:
                                st.markdown(f"<p class='success-message'>Vehicle type added: {result['type_name']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to add vehicle type')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>Please fill all fields.</p>", unsafe_allow_html=True)
        elif admin_option == "Update Parking Slots":
            with st.form(key="update_slots_form"):
                type_id_slots = st.number_input("Vehicle Type ID", min_value=1, step=1, format="%d")
                new_slots = st.number_input("New Total Slots", min_value=0, step=1, format="%d")
                submit_update_slots = st.form_submit_button("Update Slots")
                if submit_update_slots:
                    try:
                        response = requests.post(f"{API_URL}/update_slots", json={"type_id": type_id_slots, "new_slots": new_slots})
                        result = response.json()
                        if response.status_code == 200:
                            st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to update slots')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)

        elif admin_option == "Update Vehicle Cost":
            with st.form(key="update_cost_form"):
                type_id_cost = st.number_input("Vehicle Type ID", min_value=1, step=1, format="%d")
                new_cost = st.number_input("New Cost per Hour", min_value=0.0, step=0.01)
                submit_update_cost = st.form_submit_button("Update Cost")
                if submit_update_cost:
                    try:
                        response = requests.put(f"{API_URL}/update_cost", json={"type_id": type_id_cost, "new_cost": new_cost})
                        result = response.json()
                        if response.status_code == 200:
                            st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to update cost')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)

        elif admin_option == "Add Restricted Vehicle":
            with st.form(key="add_restricted_form"):
                restricted_vehicle = st.text_input("Restricted Vehicle Number")
                submit_restrict = st.form_submit_button("Add Restricted Vehicle")
                if submit_restrict:
                    if restricted_vehicle:
                        try:
                            response = requests.post(f"{API_URL}/add_restricted_vehicle", json={"vehicle_number": restricted_vehicle})
                            result = response.json()
                            if response.status_code == 200:
                                st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to add restricted vehicle')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>Please enter a vehicle number.</p>", unsafe_allow_html=True)

        elif admin_option == "Remove Restricted Vehicle":
            with st.form(key="remove_restricted_form"):
                restricted_vehicle = st.text_input("Vehicle Number to Remove")
                submit_remove = st.form_submit_button("Remove Restricted Vehicle")
                if submit_remove:
                    if restricted_vehicle:
                        try:
                            response = requests.delete(f"{API_URL}/remove_restricted_vehicle/{restricted_vehicle}")
                            result = response.json()
                            if response.status_code == 200:
                                st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to remove restricted vehicle')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>Please enter a vehicle number.</p>", unsafe_allow_html=True)

        if st.button("Logout", key="logout_button"):
            response = requests.post(f"{API_URL}/logout")
            result = response.json()
            st.session_state.admin_logged_in = False
            #st.experimental_rerun()  # Force a rerun to update the UI    st.markdown('</div>', unsafe_allow_html=True)

# Add tabs for non-admin operations
tabs = st.tabs(["Park Vehicle", "Unpark Vehicle", "View Status"])

with tabs[0]:
    st.header("Park a Vehicle")
    with st.form(key="park_form"):
        name = st.text_input("Driver Name")
        vehicle_number = st.text_input("Vehicle Number")
        type_id = st.number_input("Vehicle Type ID [bike=1 car/auto=2 truck/bus=3]", min_value=1, step=1, format="%d")
        submit_park = st.form_submit_button("Park Vehicle")
        if submit_park:
            if name and vehicle_number and type_id:
                try:
                    response = requests.post(f"{API_URL}/park", json={"name": name, "vehicle_number": vehicle_number, "type_id": type_id})
                    result = response.json()
                    if response.status_code == 200 and "message" in result:
                        st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to park vehicle')}</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='error-message'>Please enter driver name, vehicle number, and type ID.</p>", unsafe_allow_html=True)

with tabs[1]:
    st.header("Unpark a Vehicle")
    with st.form(key="unpark_form"):
        parking_id = st.number_input("Parking ID", min_value=1, step=1, format="%d")
        submit_unpark = st.form_submit_button("Unpark Vehicle")
        if submit_unpark:
            if parking_id:
                try:
                    response = requests.post(f"{API_URL}/unpark", json={"parking_id": parking_id})
                    result = response.json()
                    if response.status_code == 200 and "message" in result:
                        st.markdown(f"<p class='success-message'>{result['message']}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to unpark vehicle')}</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='error-message'>Please enter a parking ID.</p>", unsafe_allow_html=True)

with tabs[2]:
    st.header("Parking Status")
    if st.button("View Current Status"):
        try:
            response = requests.get(f"{API_URL}/status")
            if response.status_code == 200:
                status = response.json()
                if status:
                    df = pd.DataFrame([
                        {"Vehicle ID": vehicle_id, "Vehicle Type": data["vehicle"], "Total Slots": data["total"], "Occupied": data["occupied"], "Free": data["free"]}
                        for vehicle_id, data in status.items()
                    ])
                    st.table(df.style.set_table_styles([{'selector': 'tr:hover', 'props': [('background-color', '#e6f3ff')]}]))
                else:
                    st.info("No status data available.")
            else:
                st.markdown(f"<p class='error-message'>Error {response.status_code}: {response.text}</p>", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)

    st.subheader("Check Parked Vehicles by Type")
    vehicle_types = {"Truck/Bus": 1, "Car/Auto": 2, "Bikes": 3}
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Truck/Bus 🚛"):
            type_id = vehicle_types["Truck/Bus"]
            try:
                response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": type_id})
                result = response.json()
                if response.status_code == 200:
                    if isinstance(result, list) and result:
                        df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                        st.markdown(f"### Parked Vehicles (Type ID {type_id})")
                        st.dataframe(df)
                    else:
                        st.markdown(f"<p class='success-message'>No vehicles parked for type ID {type_id}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("Car/Auto 🚗"):
            type_id = vehicle_types["Car/Auto"]
            try:
                response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": type_id})
                result = response.json()
                if response.status_code == 200:
                    if isinstance(result, list) and result:
                        df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                        st.markdown(f"### Parked Vehicles (Type ID {type_id})")
                        st.dataframe(df)
                    else:
                        st.markdown(f"<p class='success-message'>No vehicles parked for type ID {type_id}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
    with col3:
        if st.button("Bikes 🚲"):
            type_id = vehicle_types["Bikes"]
            try:
                response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": type_id})
                result = response.json()
                if response.status_code == 200:
                    if isinstance(result, list) and result:
                        df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                        st.markdown(f"### Parked Vehicles (Type ID {type_id})")
                        st.dataframe(df)
                    else:
                        st.markdown(f"<p class='success-message'>No vehicles parked for type ID {type_id}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
