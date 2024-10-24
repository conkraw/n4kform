import streamlit as st

# Title of the application
st.title("NEAR4KIDS QI COLLECTION FORM")

# Initialize session state if not already done
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}
if 'page' not in st.session_state:
    st.session_state.page = "Encounter Information"  # Default page

# Page Navigation
if st.session_state.page == "Encounter Information":
    # Header for Encounter Information
    st.header("ENCOUNTER INFORMATION")
    st.subheader("Patient Information")

    # Input Form
    with st.form(key='patient_info_form'):
        # First line: Date, Time, Location
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.form_data['date'] = st.text_input("Date:", value=st.session_state.form_data.get('date', ''))
        with col2:
            st.session_state.form_data['time'] = st.text_input("Time:", value=st.session_state.form_data.get('time', ''))
        with col3:
            st.session_state.form_data['location'] = st.text_input("Location:", value=st.session_state.form_data.get('location', ''))

        # Second line: Patient Gender, Patient Dosing Weight
        col4, col5 = st.columns(2)
        with col4:
            st.session_state.form_data['patient_gender'] = st.selectbox(
                "Patient Gender:", 
                options=["Male", "Female", "Other"], 
                index=["Male", "Female", "Other"].index(st.session_state.form_data.get('patient_gender', 'Male'))
            )
        with col5:
            st.session_state.form_data['dosing_weight'] = st.selectbox(
                "Patient Dosing Weight (kg):", 
                options=list(range(1, 201)),  
                index=list(range(1, 201)).index(st.session_state.form_data.get('dosing_weight', 1))
            )

        # Third line: Diagnosis query
        st.write("AT THE TIME OF INTUBATION, did this patient have a suspected or confirmed diagnosis of an emerging epidemic/novel lung disease?")
        st.session_state.form_data['diagnosis'] = st.selectbox(
            "Diagnosis:", 
            options=["Yes", "No"], 
            index=["Yes", "No"].index(st.session_state.form_data.get('diagnosis', 'No'))
        )

        # Fourth line: Form Completed By and Pager Number
        col6, col7 = st.columns(2)
        with col6:
            st.session_state.form_data['form_completed_by'] = st.text_input(
                "Form Completed By:", 
                value=st.session_state.form_data.get('form_completed_by', '')
            )
        with col7:
            st.session_state.form_data['pager_number'] = st.text_input(
                "Pager Number:", 
                value=st.session_state.form_data.get('pager_number', '')
            )

        # Fifth line: Family Member Present and Attending Physician Present
        col8, col9 = st.columns(2)
        with col8:
            st.session_state.form_data['family_member_present'] = st.selectbox(
                "Family Member Present:", 
                options=["Yes", "No"], 
                index=["Yes", "No"].index(st.session_state.form_data.get('family_member_present', 'No'))
            )
        with col9:
            st.session_state.form_data['attending_physician_present'] = st.selectbox(
                "Attending Physician Present:", 
                options=["Yes", "No"], 
                index=["Yes", "No"].index(st.session_state.form_data.get('attending_physician_present', 'No'))
            )

        # Indications section
        st.markdown("<h2 style='text-align: center;'>INDICATIONS</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3 style='text-align: center;'>INITIAL INTUBATION</h3>", unsafe_allow_html=True)

            st.session_state.indications = st.multiselect(
                "Check as many as apply:",
                options=[
                    "Oxygen Failure (e.g. PaO2 <60 mm Hg in FIO2 >0.6 in absence of cyanotic heart disease)",
                    "Procedure (e.g. IR or MRI)",
                    "Ventilation Failure (e.g. PaCO2 > 50 mm Hg in the absence of chronic lung disease)",
                    "Frequent Apnea and Bradycardia",
                    "Upper Airway Obstruction",
                    "Therapeutic Hyperventilation (e.g. intracranial hypertension, pulmonary hypertension)",
                    "Airway Clearance",
                    "Neuromuscular Weakness (e.g. Max. negative inspiratory pressure >-20 cm H2O; vital capacity <12 – 15 ml/kg)",
                    "Emergency Drug Administration",
                    "Unstable Hemodynamics (e.g. shock)",
                    "Ongoing CPR",
                    "Absent Protective Airway Reflexes (e.g. cough, gag)",
                    "Reintubation After Unplanned Extubation",
                    "Others: ............."
                ]
            )

        with col2:
            st.markdown("<h3 style='text-align: center;'>CHANGE OF TUBE</h3>", unsafe_allow_html=True)

            col3, col4 = st.columns(2)
            with col3:
                st.session_state.type_of_change_from = st.selectbox("Type of Change From:", options=["Oral", "Nasal", "Tracheostomy"])
            with col4:
                st.session_state.type_of_change_to = st.selectbox("Type of Change To:", options=["Oral", "Nasal", "Tracheostomy"])

            st.session_state.nature_of_change = st.selectbox("Nature of Change:", 
                options=["Clinical Condition", "Immediate Post-Intubation (Exclude Tracheostomy Change)"]
            )

            st.session_state.tube_change_indications = st.multiselect(
                "Check as many as apply:",
                options=[
                    "Tube too small",
                    "Tube too big",
                    "Tube changed to cuffed tube",
                    "Tube changed to uncuffed tube",
                    "Previous tube blocked or defective",
                    "For more stable airway management",
                    "For procedure (e.g. bronchoscopy, etc)",
                    "Others: ............."
                ]
            )

        # Submit button for the form
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.page = "Course Information"  # Set next page
            st.rerun()  # Rerun the app to reflect the new page

elif st.session_state.page == "Course Information":
    st.header("COURSE INFORMATION")
    #st.write("Form data submitted:", st.session_state.form_data)
    #st.write("Indications:", st.session_state.indications)
    st.markdown("""
<p style='font-size: 14px;'>
    An <strong><u>"ENCOUNTER"</u></strong> of advanced airway management refers to the complete sequence of events leading to the placement of an advanced airway.<br>
    A <strong><u>"COURSE"</u></strong> of advanced airway management refers to <u>ONE</u> method or approach to secure an airway <strong><u>AND</u></strong> <u>ONE</u> set of medications (including premedication and induction). Each course may include one or several "attempts" by one or several providers.<br>
    An <strong><u>"ATTEMPT"</u> is a single advanced airway maneuver (e.g. tracheal intubation, LMA placement), beginning with the insertion of a device (e.g. laryngoscope or LMA device) into the patient's mouth or nose, and ending when the device (laryngoscope, LMA, or tube) is removed.</strong>
</p>
""", unsafe_allow_html=True)

    if 'attempts' not in st.session_state:
        st.session_state.attempts = {}

    # Define the number of attempts
    num_attempts = 8
    
    # Iterate over each attempt to create dropdowns
    for attempt in range(1, num_attempts + 1):
        st.header(f"Attempt {attempt}")
    
        # Who intubated
        st.session_state.attempts[f'who_intubated_{attempt}'] = st.selectbox(
            "Who intubated (Fellow, Resident, etc.):",
            options=["Select...", "Fellow", "Resident", "Attending", "Paramedic"]
        )
    
        # Discipline
        st.session_state.attempts[f'discipline_{attempt}'] = st.selectbox(
            "Discipline (ICU, ENT, Surgery, etc.):",
            options=["Select...", "ICU", "ENT", "Surgery", "Emergency Medicine"]
        )
    
        # PGY level
        st.session_state.attempts[f'pgy_level_{attempt}'] = st.selectbox(
            "PGY level (e.g., PL3, PL4, NP):",
            options=["Select...", "PL1", "PL2", "PL3", "PL4", "NP"]
        )
    
        # ETT (or LMA) size
        st.session_state.attempts[f'ett_size_{attempt}'] = st.selectbox(
            "ETT (or LMA) size:",
            options=["Select...", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5"]
        )
    
        # ETT type
        st.session_state.attempts[f'ett_type_{attempt}'] = st.selectbox(
            "ETT type (cuffed/uncuffed/NA):",
            options=["Select...", "Cuffed", "Uncuffed", "NA"]
        )
    
        # Cricoid pressure/external manipulation prior
        st.session_state.attempts[f'cricoid_prior_{attempt}'] = st.selectbox(
            "Immediately prior to this attempt, was cricoid pressure/external manipulation provided?",
            options=["Select...", "Yes", "No"]
        )
    
        # Cricoid pressure/external manipulation during
        st.session_state.attempts[f'cricoid_during_{attempt}'] = st.selectbox(
            "During this attempt, was cricoid pressure/external manipulation provided?",
            options=["Select...", "Yes", "No"]
        )
    
        # Attempt successful
        st.session_state.attempts[f'attempt_successful_{attempt}'] = st.selectbox(
            "Attempt Successful:",
            options=["Select...", "Yes", "No"]
        )
        
        # Back button to go to the previous page
        if st.button("Previous"):
            st.session_state.page = "Encounter Information"
            st.rerun()

