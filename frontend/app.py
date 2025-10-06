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
            padding-top: 20px;
        }
        
        /* Hide number input spinners */
        button.step-up {display: none;}
        button.step-down {display: none;}
        
        /* Main title styling */
        h1 {
            color: #ffffff;
            text-align: center;
            padding: 15px 0;
            font-weight: 700;
            font-size: 2.5rem;
            text-shadow: 0 3px 6px rgba(0, 0, 0, 0.4);
            margin-bottom: 20px;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50 0%, #2ecc71 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 15px;
            font-weight: 600;
            border-radius: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            width: 100%;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #45a049 0%, #27ae60 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        
        /* Input field styling - FIXED VISIBILITY */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {
            border: 2px solid #5f7fbf;
            border-radius: 10px;
            padding: 12px 15px;
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            font-size: 15px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus, 
        .stNumberInput > div > div > input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.25);
            background-color: #ffffff !important;
            outline: none;
        }
        
        .stTextInput > div > div > input::placeholder,
        .stNumberInput > div > div > input::placeholder {
            color: #7f8c8d !important;
            opacity: 0.7;
        }
        
        /* Select box styling - FIXED VISIBILITY */
        .stSelectbox > div > div > select {
            border: 2px solid #5f7fbf;
            border-radius: 10px;
            padding: 12px 15px;
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            font-size: 15px;
            font-weight: 500;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div > select:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.25);
            outline: none;
        }
        
        /* Label styling - FIXED VISIBILITY */
        label {
            font-weight: 600;
            color: #ffffff !important;
            font-size: 14px;
            margin-bottom: 8px;
            display: block;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        
        /* Admin container - Fixed top right */
        .admin-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            width: 320px;
            background: rgba(255, 255, 255, 0.97);
            backdrop-filter: blur(15px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            border: 2px solid rgba(255, 255, 255, 0.3);
            max-height: 85vh;
            overflow-y: auto;
        }
        
        .admin-container label {
            color: #2c3e50 !important;
            text-shadow: none;
        }
        
        .admin-container h3 {
            color: #2c3e50 !important;
            margin-top: 0;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
        }
        
        .admin-container .stMarkdown {
            color: #2c3e50;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
            margin-top: 20px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.15);
            border-radius: 10px 10px 0 0;
            padding: 12px 24px;
            font-weight: 600;
            border: none;
            color: #ffffff;
            transition: all 0.3s ease;
            font-size: 15px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.95);
            color: #2c3e50;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Form styling */
        .stForm {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.25);
            margin-bottom: 20px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Table styling */
        .dataframe {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            width: 100%;
            font-size: 14px;
            background-color: white;
        }
        
        .dataframe thead th {
            background: linear-gradient(135deg, #4CAF50 0%, #2ecc71 100%);
            color: white;
            font-weight: 600;
            padding: 14px;
        }
        
        .dataframe tbody td {
            color: #2c3e50;
            padding: 12px;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        
        .dataframe tbody tr:hover {
            background-color: #e8f5e9;
        }
        
        /* Success and error messages */
        .success-message {
            color: #ffffff;
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            padding: 12px 16px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            margin: 12px 0;
            box-shadow: 0 4px 8px rgba(46, 204, 113, 0.3);
        }
        
        .error-message {
            color: #ffffff;
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            padding: 12px 16px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            margin: 12px 0;
            box-shadow: 0 4px 8px rgba(231, 76, 60, 0.3);
        }
        
        /* Header styling */
        h2, h3 {
            color: #ffffff;
            font-weight: 600;
            margin-bottom: 15px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            padding-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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
            background: rgba(76, 175, 80, 0.7);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(76, 175, 80, 0.9);
        }
        
        /* Info text */
        .info-text {
            color: #ecf0f1;
            font-size: 16px;
            margin: 10px 0 20px 0;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
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

st.title("🚗 Parking Management System")

# Session state for admin login
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# Admin Section - Fixed in top-right corner (SEPARATE FROM MAIN CONTENT)
with st.container():
    st.markdown('<div class="admin-container">', unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        if not st.session_state.show_login:
            if st.button("🔑 Admin Login", key="login_toggle"):
                st.session_state.show_login = True
        
        if st.session_state.show_login:
            with st.form(key="login_form"):
                st.markdown("**Admin Login**")
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                submit_login = st.form_submit_button("Login")
                if submit_login:
                    if username and password:
                        try:
                            response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                            result = response.json()
                            if response.status_code == 200 and "message" in result:
                                st.session_state.admin_logged_in = True
                                st.session_state.show_login = False
                                st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                                st.rerun()
                            else:
                                st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Authentication failed')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>❌ Please enter both username and password.</p>", unsafe_allow_html=True)
    else:
        st.markdown("### ✅ Admin Panel")
        st.markdown("**Logged in successfully**")
        
        admin_option = st.selectbox(
            "Admin Actions",
            ["Select Action", "Update Parking Slots", "Add Vehicle Type", "Update Vehicle Cost", 
             "Add Restricted Vehicle", "Remove Restricted Vehicle"],
            key="admin_dropdown"
        )
        
        if admin_option == "Add Vehicle Type":
            with st.form(key="add_vehicle_form"):
                type_name = st.text_input("Vehicle Type Name", placeholder="e.g., SUV")
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
                                st.markdown(f"<p class='success-message'>✅ Vehicle type added: {result['type_name']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to add vehicle type')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>❌ Please fill all fields.</p>", unsafe_allow_html=True)
        
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
                            st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to update slots')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
        
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
                            st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to update cost')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
        
        elif admin_option == "Add Restricted Vehicle":
            with st.form(key="add_restricted_form"):
                restricted_vehicle = st.text_input("Restricted Vehicle Number", placeholder="e.g., KA-01-XX-9999")
                submit_restrict = st.form_submit_button("Add Restricted Vehicle")
                if submit_restrict:
                    if restricted_vehicle:
                        try:
                            response = requests.post(f"{API_URL}/add_restricted_vehicle", json={"vehicle_number": restricted_vehicle})
                            result = response.json()
                            if response.status_code == 200:
                                st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to add restricted vehicle')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>❌ Please enter a vehicle number.</p>", unsafe_allow_html=True)
        
        elif admin_option == "Remove Restricted Vehicle":
            with st.form(key="remove_restricted_form"):
                restricted_vehicle = st.text_input("Vehicle Number to Remove", placeholder="e.g., KA-01-XX-9999")
                submit_remove = st.form_submit_button("Remove Restricted Vehicle")
                if submit_remove:
                    if restricted_vehicle:
                        try:
                            response = requests.delete(f"{API_URL}/remove_restricted_vehicle/{restricted_vehicle}")
                            result = response.json()
                            if response.status_code == 200:
                                st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                            else:
                                st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to remove restricted vehicle')}</p>", unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='error-message'>❌ Please enter a vehicle number.</p>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", key="logout_button"):
            try:
                response = requests.post(f"{API_URL}/logout")
                st.session_state.admin_logged_in = False
                st.rerun()
            except:
                st.session_state.admin_logged_in = False
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content container (WITHOUT admin section inside)
with st.container():
    
    # Add tabs for non-admin operations
    tabs = st.tabs(["🚗 Park Vehicle", "🚪 Unpark Vehicle", "📊 View Status"])
    
    with tabs[0]:
        st.header("Park a Vehicle")
        with st.form(key="park_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Driver Name", placeholder="Enter driver name")
                vehicle_number = st.text_input("Vehicle Number", placeholder="e.g., KA-01-AB-1234")
            with col2:
                type_id = st.selectbox(
                    "Vehicle Type",
                    options=[1, 2, 3],
                    format_func=lambda x: {1: "🚲 Bike", 2: "🚗 Car/Auto", 3: "🚛 Truck/Bus"}[x]
                )
            submit_park = st.form_submit_button("🚗 Park Vehicle")
            if submit_park:
                if name and vehicle_number:
                    try:
                        response = requests.post(f"{API_URL}/park", json={"name": name, "vehicle_number": vehicle_number, "type_id": type_id})
                        result = response.json()
                        if response.status_code == 200 and "message" in result:
                            st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to park vehicle')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p class='error-message'>❌ Please enter driver name and vehicle number.</p>", unsafe_allow_html=True)
    
    with tabs[1]:
        st.header("Unpark a Vehicle")
        with st.form(key="unpark_form"):
            parking_id = st.number_input("Parking ID", min_value=1, step=1, format="%d", placeholder="Enter parking ID")
            submit_unpark = st.form_submit_button("🚪 Unpark Vehicle")
            if submit_unpark:
                if parking_id:
                    try:
                        response = requests.post(f"{API_URL}/unpark", json={"parking_id": parking_id})
                        result = response.json()
                        if response.status_code == 200 and "message" in result:
                            st.markdown(f"<p class='success-message'>✅ {result['message']}</p>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to unpark vehicle')}</p>", unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
                else:
                    st.markdown("<p class='error-message'>❌ Please enter a parking ID.</p>", unsafe_allow_html=True)
    
    with tabs[2]:
        st.header("Parking Status")
        
        # Overall Status
        if st.button("🔄 Refresh Overall Status"):
            try:
                response = requests.get(f"{API_URL}/status")
                if response.status_code == 200:
                    status = response.json()
                    if status:
                        df = pd.DataFrame([
                            {"Vehicle Type": data["vehicle"], "Total Slots": data["total"], "Occupied": data["occupied"], "Free": data["free"]}
                            for vehicle_id, data in status.items()
                        ])
                        st.subheader("Overall Parking Status")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No status data available.")
                else:
                    st.markdown(f"<p class='error-message'>❌ Error {response.status_code}: {response.text}</p>", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
        
        # Parked Vehicles by Type
        st.subheader("Check Parked Vehicles")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚛 Truck/Bus", use_container_width=True):
                try:
                    response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": 3})
                    result = response.json()
                    if response.status_code == 200:
                        if isinstance(result, list) and result:
                            df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.markdown(f"<p class='success-message'>✅ No Vehicles Parked</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
        
        with col2:
            if st.button("🚗 Car/Auto", use_container_width=True):
                try:
                    response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": 2})
                    result = response.json()
                    if response.status_code == 200:
                        if isinstance(result, list) and result:
                            df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.markdown(f"<p class='success-message'>✅ No Vehicles Parked</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)
        
        with col3:
            if st.button("🚲 Bikes", use_container_width=True):
                try:
                    response = requests.post(f"{API_URL}/parking_id_status", json={"type_id": 1})
                    result = response.json()
                    if response.status_code == 200:
                        if isinstance(result, list) and result:
                            df = pd.DataFrame(result)[["name", "vehicle_number", "in_time"]]
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.markdown(f"<p class='success-message'>✅ No Vehicles Parked</p>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p class='error-message'>❌ {result.get('detail', 'Failed to fetch status')}</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"<p class='error-message'>❌ Failed to connect to backend: {e}</p>", unsafe_allow_html=True)