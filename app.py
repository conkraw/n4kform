import streamlit as st
st.set_page_config(layout="wide")

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

        # Diagnosis query
        st.write("AT THE TIME OF INTUBATION, did this patient have a suspected or confirmed diagnosis of an emerging epidemic/novel lung disease?")
        st.session_state.form_data['diagnosis'] = st.selectbox(
            "Diagnosis:", 
            options=["Yes", "No"], 
            index=["Yes", "No"].index(st.session_state.form_data.get('diagnosis', 'No'))
        )

        # Form Completed By and Pager Number
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

        # Family Member Present and Attending Physician Present
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

    # Displaying the previously submitted data if necessary
    st.write("Form data submitted:", st.session_state.form_data)

    # Instructions
    st.markdown("""
    <p style='font-size: 14px;'>
        An <strong><u>"ENCOUNTER"</u></strong> of advanced airway management refers to the complete sequence of events leading to the placement of an advanced airway.<br>
        A <strong><u>"COURSE"</u></strong> of advanced airway management refers to <u>ONE</u> method or approach to secure an airway <strong><u>AND</u></strong> <u>ONE</u> set of medications (including premedication and induction). Each course may include one or several "attempts" by one or several providers.<br>
        An <strong><u>"ATTEMPT"</u></strong> is a single advanced airway maneuver (e.g. tracheal intubation, LMA placement), beginning with the insertion of a device (e.g. laryngoscope or LMA device) into the patient's mouth or nose, and ending when the device (laryngoscope, LMA, or tube) is removed.
    </p>
    """, unsafe_allow_html=True)

    # Initialize attempts data if not already done
    if 'attempts' not in st.session_state:
        st.session_state.attempts = {f'Attempt {i}': {
            'who_intubated': None,
            'discipline': None,
            'pgy_level': None,
            'ett_size': None,
            'ett_type': None,
            'cricoid_prior': None,
            'cricoid_during': None,
            'attempt_successful': None,
        } for i in range(1, 9)}

    attempt_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Define row headers
    row_headers = ["Attempts for this Course",
        "Who Intubated",
        "Discipline",
        "PGY Level",
        "ETT (or LMA) Size",
        "ETT Type",
        "Cricoid Pressure Prior",
        "Cricoid Pressure During",
        "Attempt Successful"
    ]
        
    # Create the table-like layout
    for row_header in row_headers:
        cols = st.columns(len(attempt_numbers) + 1)  # Create columns for attempts plus one for the row header
        
        with cols[0]:  # Row header
            st.text_input("", value=row_header, disabled=True)
        
        for attempt in attempt_numbers:
            with cols[attempt]:  # Each attempt column
                if row_header == "Attempts for this Course":
                    st.session_state.attempts[f'Attempt {attempt}']['who_intubated'] = st.selectbox(
                        "", ["", "Fellow", "Resident", "Attending", "Paramedic"],
                        key=f'who_intubated_{attempt}'
                    )
                elif row_header == "Who Intubated":
                    st.session_state.attempts[f'Attempt {attempt}']['who_intubated'] = st.selectbox(
                        "", ["", "Fellow", "Resident", "Attending", "Paramedic"],
                        key=f'who_intubated_{attempt}'
                    )
                elif row_header == "Discipline":
                    st.session_state.attempts[f'Attempt {attempt}']['discipline'] = st.selectbox(
                        "", ["", "ICU", "ENT", "Surgery", "Emergency Medicine"],
                        key=f'discipline_{attempt}'
                    )
                elif row_header == "PGY Level":
                    st.session_state.attempts[f'Attempt {attempt}']['pgy_level'] = st.selectbox(
                        "", ["", "PL1", "PL2", "PL3", "PL4", "NP"],
                        key=f'pgy_level_{attempt}'
                    )
                elif row_header == "ETT (or LMA) Size":
                    st.session_state.attempts[f'Attempt {attempt}']['ett_size'] = st.selectbox(
                        "", ["", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0", "5.5"],
                        key=f'ett_size_{attempt}'
                    )
                elif row_header == "ETT Type":
                    st.session_state.attempts[f'Attempt {attempt}']['ett_type'] = st.selectbox(
                        "", ["", "Cuffed", "Uncuffed", "NA"],
                        key=f'ett_type_{attempt}'
                    )
                elif row_header == "Cricoid Pressure Prior":
                    st.session_state.attempts[f'Attempt {attempt}']['cricoid_prior'] = st.selectbox(
                        "", ["", "Yes", "No"],
                        key=f'cricoid_prior_{attempt}'
                    )
                elif row_header == "Cricoid Pressure During":
                    st.session_state.attempts[f'Attempt {attempt}']['cricoid_during'] = st.selectbox(
                        "", ["", "Yes", "No"],
                        key=f'cricoid_during_{attempt}'
                    )
                elif row_header == "Attempt Successful":
                    st.session_state.attempts[f'Attempt {attempt}']['attempt_successful'] = st.selectbox(
                        "", ["", "Yes", "No"],
                        key=f'attempt_successful_{attempt}'
                    )

    # Back button to go to the previous page
    if st.button("Previous"):
        st.session_state.page = "Encounter Information"
        st.rerun()

