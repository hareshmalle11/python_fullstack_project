import streamlit as st
import requests
import pandas as pd

# FastAPI backend URL
API_URL = "https://park-backend-5vgz.onrender.com"

# Inject custom CSS
st.markdown("""
    <style>
        /* Global styles */
        .stApp {
            background: linear-gradient(135deg, #0c2461 0%, #1e3799 50%, #4a69bd 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #f5f6fa;
        }
        
        /* Hide number input spinners */
        button.step-up {display: none;}
        button.step-down {display: none;}
        
        /* Main title styling */
        h1 {
            color: #f5f6fa;
            text-align: center;
            padding: 20px;
            font-weight: 700;
            font-size: 2.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 10px;
            background: linear-gradient(90deg, #4CAF50, #2ecc71);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50 0%, #2ecc71 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #45a049 0%, #27ae60 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {
            border: 2px solid #4a69bd;
            border-radius: 8px;
            padding: 12px 16px;
            background-color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stNumberInput > div > div > input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
            background-color: white;
        }
        
        /* Select box styling */
        .stSelectbox > div > div > select {
            border: 2px solid #4a69bd;
            border-radius: 8px;
            padding: 12px 16px;
            background-color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div > select:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
            background-color: white;
        }
        
        /* Admin container styling */
        .admin-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            width: 280px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #2c3e50;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            font-weight: 600;
            border: none;
            color: #f5f6fa;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.9);
            color: #2c3e50;
        }
        
        /* Form styling */
        .stForm {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Table styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .dataframe thead th {
            background: linear-gradient(135deg, #4CAF50 0%, #2ecc71 100%);
            color: white;
            font-weight: 600;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        .dataframe tbody tr:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        
        /* Success and error messages */
        .success-message {
            color: #2ecc71;
            background-color: rgba(46, 204, 113, 0.1);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #2ecc71;
            font-weight: 600;
        }
        
        .error-message {
            color: #e74c3c;
            background-color: rgba(231, 76, 60, 0.1);
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            font-weight: 600;
        }
        
        /* Column styling for buttons */
        .stColumns {
            gap: 16px;
        }
        
        .stColumn {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Header styling */
        .stHeader {
            color: #f5f6fa;
            font-weight: 700;
            margin-bottom: 20px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 10px;
        }
        
        /* Info box styling */
        .stInfo {
            background: rgba(52, 152, 219, 0.2);
            border: 1px solid rgba(52, 152, 219, 0.5);
            border-radius: 8px;
            padding: 16px;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(76, 175, 80, 0.6);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(76, 175, 80, 0.8);
        }
        
        /* Animation for form submission */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .stForm {
            animation: fadeIn 0.5s ease;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .admin-container {
                position: relative;
                width: 100%;
                top: 0;
                right: 0;
                margin-bottom: 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
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
<<<<<<< HEAD
                        st.markdown(f"<p class='success-message'>No vehicles parked yet</p>", unsafe_allow_html=True)
=======
                        st.markdown(f"<p class='success-message'>No Vehicles Parked till Now</p>", unsafe_allow_html=True)
>>>>>>> 6b54c86d940710d49d64d58e131c9a17dbb22c8d
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
<<<<<<< HEAD
                        st.markdown(f"<p class='success-message'>No vehicles parked yet</p>", unsafe_allow_html=True)
=======
                        st.markdown(f"<p class='success-message'>No vehicles Parked till Now</p>", unsafe_allow_html=True)
>>>>>>> 6b54c86d940710d49d64d58e131c9a17dbb22c8d
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
<<<<<<< HEAD
                        st.markdown(f"<p class='success-message'>No vehicles parked yet</p>", unsafe_allow_html=True)
=======
                        st.markdown(f"<p class='success-message'>No Vehicles Parked till Now</p>", unsafe_allow_html=True)
>>>>>>> 6b54c86d940710d49d64d58e131c9a17dbb22c8d
                else:
                    st.markdown(f"<p class='error-message'>{result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<p class='error-message'>Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
