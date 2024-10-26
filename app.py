import streamlit as st
import datetime

st.set_page_config(layout="wide")

def reset_inputx(default_value, key):
    # Initialize the key in session state if it doesn't exist
    if key not in st.session_state:
        st.session_state[key] = default_value
    
    # Create the text input and get the current value
    current_value = st.text_input("", key=key, value=st.session_state[key])
    
    # Update session state if the input changes
    if current_value != st.session_state[key]:
        st.session_state[key] = current_value
    
    return current_value

    
def reset_input(default_value, key, width="100%", height="40px"):
    # Add custom CSS for input styling
    st.markdown(
        f"""
        <style>
        .reset-input-container {{
            display: flex;              /* Use flexbox for centering */
            justify-content: center;    /* Center horizontally */
            align-items: center;        /* Center vertically if needed */
        }}
        .reset-input {{
            font-size: 12px !important;  /* Adjust the font size */
            padding: 10px;                /* Adjust padding */
            width: {width};              /* Control width */
            height: {height};            /* Control height */
            box-sizing: border-box;      /* Ensure padding doesn't affect width */
            border: 1px solid #ccc;      /* Border */
            border-radius: 4px;          /* Rounded corners for aesthetics */
            background-color: #f9f9f9;   /* Light background */
            font-weight: bold;            /* Make text bold */
            text-align: center;           /* Center the text */
            display: block;               /* Make it a block element for centering */
            margin: 0 auto;              /* Center the input box */
        }}
        </style>
        """, unsafe_allow_html=True
    )

    # Initialize session state if not already done
    if key not in st.session_state:
        st.session_state[key] = default_value

    current_value = st.session_state[key]

    # Create a styled input field wrapped in a container for centering
    input_html = f"""
        <div class="reset-input-container">
            <input class="reset-input" type="text" value="{current_value}" 
                   oninput="this.value=this.value.replace(/</g,'&lt;').replace(/>/g,'&gt;')" />
        </div>
    """
    
    # Render the HTML input field
    st.markdown(input_html, unsafe_allow_html=True)

    # Update session state if the input value changes
    if st.session_state[key] != current_value:
        st.session_state[key] = current_value
    
    return current_value

def custom_input(key, default_value="", input_type="text"):
    # Initialize session state if not already done
    if key not in st.session_state:
        st.session_state[key] = default_value

    # Create a Streamlit text input and center it with CSS
    st.markdown(
        """
        <style>
        .custom-input {
            display: flex;
            justify-content: center;
        }
        .custom-input input {
            width: 100%;  /* Adjust width as needed */
            max-width: 300px;  /* Set a maximum width */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Create a centered input field
    input_value = st.text_input(
        "", 
        value=st.session_state[key], 
        key=key,
        placeholder="", 
        help="Enter your text here",
        label_visibility="collapsed"  # Hide label to avoid double display
    )

    # Update session state with user input if changed
    if input_value != st.session_state[key]:
        st.session_state[key] = input_value
    
    return st.session_state[key]



def centered_input(default_value, key, width="100%", height="40px"):
    # Add custom CSS for centered input styling
    st.markdown(
        f"""
        <style>
        .centered-input {{
            font-size: 12px !important;  /* Adjust the font size */
            padding: 8px;                /* Adjust padding */
            width: {width};              /* Control width */
            height: {height};            /* Control height */
            box-sizing: border-box;      /* Ensure padding doesn't affect width */
            border: 1px solid #ccc;      /* Border */
            border-radius: 4px;          /* Rounded corners for aesthetics */
            background-color: #f9f9f9;   /* Light background */
            font-weight: bold;            /* Make text bold */
            text-align: center;           /* Center the text */
            display: block;               /* Make it a block element for centering */
            margin: 0 auto;              /* Center the input box */
        }}
        </style>
        """, unsafe_allow_html=True
    )

    # Initialize session state if not already done
    if key not in st.session_state:
        st.session_state[key] = default_value

    current_value = st.session_state[key]

    # Create a styled input field
    input_html = f"""
        <input class="centered-input" type="text" value="{current_value}" 
               oninput="this.value=this.value.replace(/</g,'&lt;').replace(/>/g,'&gt;')" />
    """
    
    # Render the HTML input field
    st.markdown(input_html, unsafe_allow_html=True)

    # Update session state if the input value changes
    if st.session_state[key] != current_value:
        st.session_state[key] = current_value
    return current_value

def question_box(label):
    # Add custom CSS for the question box styling
    st.markdown(
        """
        <style>
        .question-box {
            font-size: 14px !important;  /* Adjust the font size */
            padding: 10px;                /* Adjust padding */
            margin: 10px 0;              /* Margin for spacing */
            border: 1px solid #ccc;      /* Border */
            border-radius: 4px;          /* Rounded corners */
            background-color: #f0f8ff;   /* Light background */
            font-weight: bold;            /* Make text bold */
            text-align: left;             /* Align text to the left */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Create a styled div with the question label
    input_html = f"""
        <div class="question-box">
            {label}
        </div>
    """
    
    st.markdown(input_html, unsafe_allow_html=True)


import streamlit as st
import datetime

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
            st.session_state.form_data['date'] = st.date_input("Date:", value=st.session_state.form_data.get('date', datetime.date.today()))
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

        # Next button
        submit_button = st.form_submit_button("Next")
        if submit_button:
            st.session_state.page = "Indications"  # Navigate to the next page
            st.rerun() 

elif st.session_state.page == "Indications":
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
            ],
            default=st.session_state.get('indications', [])
        )

    with col2:
        st.markdown("<h3 style='text-align: center;'>CHANGE OF TUBE</h3>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.type_of_change_from = st.selectbox("Type of Change From:", options=["Oral", "Nasal", "Tracheostomy"], index=["Oral", "Nasal", "Tracheostomy"].index(st.session_state.get('type_of_change_from', 'Oral')))
        with col4:
            st.session_state.type_of_change_to = st.selectbox("Type of Change To:", options=["Oral", "Nasal", "Tracheostomy"], index=["Oral", "Nasal", "Tracheostomy"].index(st.session_state.get('type_of_change_to', 'Oral')))

        st.session_state.nature_of_change = st.selectbox("Nature of Change:", 
            options=["Clinical Condition", "Immediate Post-Intubation (Exclude Tracheostomy Change)"],
            index=["Clinical Condition", "Immediate Post-Intubation (Exclude Tracheostomy Change)"].index(st.session_state.get('nature_of_change', 'Clinical Condition'))
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
            ],
            default=st.session_state.get('tube_change_indications', [])
        )

    # Navigation buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Encounter Information"  # Navigate back to the previous page
            st.rerun()  # Rerun the app to reflect the new page

    with col_next:
        if st.button("Next"):
            st.session_state.page = "Course Information"  # Set next page
            st.rerun() 

elif st.session_state.page == "Course Information":
    st.header("COURSE INFORMATION")

    # Instructions
    st.markdown("""
    <p style='font-size: 14px;'>
        An <strong><u>"ENCOUNTER"</u></strong> of advanced airway management refers to the complete sequence of events leading to the placement of an advanced airway.<br>
        A <strong><u>"COURSE"</u></strong> of advanced airway management refers to <u>ONE</u> method or approach to secure an airway <strong><u>AND</u></strong> <u>ONE</u> set of medications (including premedication and induction). Each course may include one or several "attempts" by one or several providers.<br>
        An <strong><u>"ATTEMPT"</u></strong> is a single advanced airway maneuver (e.g. tracheal intubation, LMA placement), beginning with the insertion of a device (e.g. laryngoscope or LMA device) into the patient's mouth or nose, and ending when the device (laryngoscope, LMA, or tube) is removed.
    </p>
    """, unsafe_allow_html=True)

    # Initialize session state if not already done
    if 'attempts' not in st.session_state:
        st.session_state.attempts = {f'Attempt {i}': {
            'who_intubated': "",
            'discipline': "",
            'pgy_level': "",
            'ett_size': "",
            'ett_type': "",
            'cricoid_prior': "",
            'cricoid_during': "",
            'attempt_successful': "",
        } for i in range(1, 9)}

    # Define the row headers
    row_headers = [
        "Attempts for this COURSE",
        "Who intubated (Fellow, Resident, etc)",
        "Discipline (ICU, ENT, Surgery, etc)",
        "PGY level (3rd year resident = PL3, 1st year fellow = PL4, NP=yrs as NP, etc.)",
        "ETT (or LMA) Size",
        "ETT type: cuffed/uncuffed/ NA",
        "Immediately prior to this attempt was cricoid pressure/external laryngeal manipulation provided?",
        "During this attempt, was cricoid pressure/external laryngeal manipulation provided?",
        "Attempt Successful: Yes/No"
    ]

    # Define attempt numbers
    attempt_numbers = range(1, 9)

    # Create the table-like layout
    for row_header in row_headers:
        cols = st.columns(len(attempt_numbers) + 1)  # Create extra column for headers
        with cols[0]:  # Column for row headers
            reset_input(row_header, f"header_{row_header}")  
            
        for attempt in attempt_numbers:
            with cols[attempt]:  # Adjust for 1-based indexing
                attempt_key = f'Attempt {attempt}'
                if row_header == "Attempts for this COURSE":
                    centered_input(str(attempt), f"attempt_course_{attempt}", width='50px', height='40px') 
                
                elif row_header == "Who intubated (Fellow, Resident, etc)":
                    st.session_state.attempts[attempt_key]['who_intubated'] = custom_input(
                        f'who_intubated_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['who_intubated']
                    )
                elif row_header == "Discipline (ICU, ENT, Surgery, etc)":
                    st.session_state.attempts[attempt_key]['discipline'] = custom_input(
                        f'discipline_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['discipline']
                    )
                elif row_header == "PGY level (3rd year resident = PL3, 1st year fellow = PL4, NP=yrs as NP, etc.)":
                    st.session_state.attempts[attempt_key]['pgy_level'] = custom_input(
                        f'pgy_level_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['pgy_level']
                    )
                elif row_header == "ETT (or LMA) Size":
                    st.session_state.attempts[attempt_key]['ett_size'] = custom_input(
                        f'ett_size_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['ett_size']
                    )
                elif row_header == "ETT type: cuffed/uncuffed/ NA":
                    st.session_state.attempts[attempt_key]['ett_type'] = custom_input(
                        f'ett_type_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['ett_type']
                    )
                elif row_header == "Immediately prior to this attempt was cricoid pressure/external laryngeal manipulation provided?":
                    st.session_state.attempts[attempt_key]['cricoid_prior'] = custom_input(
                        f'cricoid_prior_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['cricoid_prior']
                    )
                elif row_header == "During this attempt, was cricoid pressure/external laryngeal manipulation provided?":
                    st.session_state.attempts[attempt_key]['cricoid_during'] = custom_input(
                        f'cricoid_during_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['cricoid_during']
                    )
                elif row_header == "Attempt Successful: Yes/No":
                    st.session_state.attempts[attempt_key]['attempt_successful'] = custom_input(
                        f'attempt_successful_{attempt}',
                        default_value=st.session_state.attempts[attempt_key]['attempt_successful']
                    )

    # Navigation buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Indications"  # Go back to the previous page
            st.rerun()  # Rerun the app to reflect the new page

    with col_next:
        if st.button("Next"):
            st.session_state.page = "Difficult Airway Evaluation"  # Set next page
            st.rerun()  # Rerun the app to reflect the new page

elif st.session_state.page == "Difficult Airway Evaluation":
    st.markdown("### Difficult Airway Evaluations (Choose one in each category):")
    
    # Define questions and options
    questions = [
        ("Evaluation done before or after this course is completed?", ['Select Category 1', 'BEFORE', 'AFTER']),
        ("Known prior history of difficult airway?", ['Select Category 2', 'YES', 'NO']),
        ("Any Limited Neck Extension or (Maximal with or without sedation/paralytics) Severe Reduction?", ['Select Category 3', 'YES', 'NO']),
        ("Widest Mouth Opening – How many Patient’s fingers between gum/incisors?", ['Select Category 4', '0 – 2', '≥ 3']),
        ("Thyromental space – Patient’s fingers between chin and thyroid cartilage?", ['Select Category 5', '0 - 2', '≥ 3']),
        ("Evidence of Upper Airway Obstruction or Anatomical Barrier to visualize glottic opening?", ['Select Category 6', 'YES', 'NO']),
        ("Midfacial Hypoplasia?", ['Select Category 7', 'YES', 'NO']),
        ("Any other signs of difficult airway exist?", ['Select Category 8', 'YES', 'NO']),
    ]

    # Ensure session state is initialized for each question
    for idx, (question, options) in enumerate(questions):
        key = f"evaluation_{idx}"
        if key not in st.session_state:
            st.session_state[key] = f'Select Category {idx + 1}' 

    # Create the layout for questions
    for idx, (question, options) in enumerate(questions):
        cols = st.columns([4, 1])
        
        with cols[0]:
            question_box(f"{idx + 1}. {question}")  # Display question
            
        with cols[1]:
            # Create selectbox with options
            selected_option = st.selectbox(
                "",
                options=options,
                index=options.index(st.session_state[f"evaluation_{idx}"]),  # Get current value
                key=f"evaluation_{idx}_selectbox"  # Unique key for each selectbox
            )

            # Update session state
            st.session_state[f"evaluation_{idx}"] = selected_option

    # Difficult to Bag/Mask Ventilate
    st.markdown("### Difficult to Bag/Mask Ventilate? (Select ONE only)")
    if "difficult_to_bag" not in st.session_state:
        st.session_state["difficult_to_bag"] = 'Select Whether the Patient Was Difficult to Bag/Mask Ventilate' 
    
    difficult_to_bag = st.selectbox(
        "",
        options=['Select Whether the Patient Was Difficult to Bag/Mask Ventilate', 'Yes', 'No', 'Not applicable (bag-mask ventilation not given)'],
        index=['Select Whether the Patient Was Difficult to Bag/Mask Ventilate', 'Yes', 'No', 'Not applicable (bag-mask ventilation not given)'].index(st.session_state["difficult_to_bag"]),
        key="difficult_to_bag_selectbox"  # Unique key for this selectbox
    )
    
    # Update session state
    st.session_state["difficult_to_bag"] = difficult_to_bag
    
    
    # Known cyanotic heart disease
    st.markdown("### Known cyanotic heart disease (R to L shunt)? (Select ONE only)")
    if "cyanotic" not in st.session_state:
        st.session_state["cyanotic"] = 'Select if Patient With Known cyanotic heart disease'
    
    cyanotic = st.selectbox(
        "",
        options=['Select if Patient With Known cyanotic heart disease', 'Yes', 'No'],
        index=['Select if Patient With Known cyanotic heart disease', 'Yes', 'No'].index(st.session_state["cyanotic"]),
        key="cyanotic_selectbox"  # Unique key for this selectbox
    )
    
    # Update session state
    st.session_state["cyanotic"] = cyanotic


    # Navigation buttons
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Course Information"  # Go back to the previous page
            st.rerun()  # Rerun the app to reflect the new page

    with col_next:
        if st.button("Next"):
            st.session_state.page = "Medications"  # Set next page
            st.rerun()  # Rerun the app to reflect the new page

elif st.session_state.page == "Medications":
    st.header("MEDICATIONS")

    # Instructions
    st.markdown("""
    <p style='font-size: 14px;'>
        If no drugs are used, select the corresponding option. Otherwise, fill in the dosages for the medications listed below.
    </p>
    """, unsafe_allow_html=True)

    # Initialize session state variables if not already set
    default_values = {
        "no_drugs": "NO DRUGS USED",
        "atropine_dose": "",
        "glycopyrrolate_dose": "",
        "fentanyl_dose": "",
        "lidocaine_dose": "",
        "vecuronium_dose": "",
        "rocuronium_dose": "",
        "succinylcholine_dose": "",
        "pancuronium_dose": "",
        "cisatracuronium_dose": "",
        "propofol_dose": "",
        "etomidate_dose": "",
        "ketamine_dose": "",
        "midazolam_dose": "",
        "thiopental_dose": "",
        "vecuronium_paralysis_dose": "",
        "atropine_indications": [],
        "glycopyrrolate_indications": [],
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Print the session state for debugging
    st.write("Session State:", st.session_state)

    # Select box for drugs used
    no_drugs = st.selectbox("Have any drugs been used?", ["NO DRUGS USED", "DRUGS USED"], 
                            index=["NO DRUGS USED", "DRUGS USED"].index(st.session_state.no_drugs))
    
    st.session_state.no_drugs = no_drugs  # Save the selection

    if no_drugs == "DRUGS USED":
        # Create columns for dosages
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### Pretreatment Dosage")
            # Create input fields with unique keys
            atropine_input = st.text_input("mg Atropine", value=st.session_state.atropine_dose, key="atropine_dose_input")
            glycopyrrolate_input = st.text_input("mcg Glycopyrrolate", value=st.session_state.glycopyrrolate_dose, key="glycopyrrolate_dose_input")
            fentanyl_input = st.text_input("mcg Fentanyl", value=st.session_state.fentanyl_dose, key="fentanyl_dose_input")
            lidocaine_input = st.text_input("mg Lidocaine", value=st.session_state.lidocaine_dose, key="lidocaine_dose_input")
            vecuronium_input = st.text_input("mg Vecuronium", value=st.session_state.vecuronium_dose, key="vecuronium_dose_input")

        with col2:
            st.markdown("### Paralysis Dosage")
            rocuronium_input = st.text_input("mg Rocuronium", value=st.session_state.rocuronium_dose, key="rocuronium_dose_input")
            succinylcholine_input = st.text_input("mg Succinylcholine", value=st.session_state.succinylcholine_dose, key="succinylcholine_dose_input")
            vecuronium_paralysis_input = st.text_input("mg Vecuronium", value=st.session_state.vecuronium_paralysis_dose, key="vecuronium_paralysis_dose_input")
            pancuronium_input = st.text_input("mg Pancuronium", value=st.session_state.pancuronium_dose, key="pancuronium_dose_input")
            cisatracuronium_input = st.text_input("mg Cisatracuronium", value=st.session_state.cisatracuronium_dose, key="cisatracuronium_dose_input")

        with col3:
            st.markdown("### Induction Dosage")
            propofol_input = st.text_input("mg Propofol", value=st.session_state.propofol_dose, key="propofol_dose_input")
            etomidate_input = st.text_input("mg Etomidate", value=st.session_state.etomidate_dose, key="etomidate_dose_input")
            ketamine_input = st.text_input("mg Ketamine", value=st.session_state.ketamine_dose, key="ketamine_dose_input")
            midazolam_input = st.text_input("mg Midazolam", value=st.session_state.midazolam_dose, key="midazolam_dose_input")
            thiopental_input = st.text_input("mg Thiopental", value=st.session_state.thiopental_dose, key="thiopental_dose_input")

        # Atropine Indication
        st.markdown("### Atropine Indication")
        atropine_indications = st.multiselect("Select indications for Atropine:", 
            ["Premed for TI", "Treatment of Bradycardia"],
            default=st.session_state.atropine_indications)
        
        # Glycopyrrolate Indication
        st.markdown("### Glycopyrrolate Indication")
        glycopyrrolate_indications = st.multiselect("Select indications for Glycopyrrolate:", 
            ["Premed for TI", "Treatment of Bradycardia"],
            default=st.session_state.glycopyrrolate_indications)

        # Update session state only after inputs have been collected
        if st.button("Submit"):
            st.session_state.atropine_dose = atropine_input
            st.session_state.glycopyrrolate_dose = glycopyrrolate_input
            st.session_state.fentanyl_dose = fentanyl_input
            st.session_state.lidocaine_dose = lidocaine_input
            st.session_state.vecuronium_dose = vecuronium_input
            st.session_state.rocuronium_dose = rocuronium_input
            st.session_state.succinylcholine_dose = succinylcholine_input
            st.session_state.vecuronium_paralysis_dose = vecuronium_paralysis_input
            st.session_state.pancuronium_dose = pancuronium_input
            st.session_state.cisatracuronium_dose = cisatracuronium_input
            st.session_state.propofol_dose = propofol_input
            st.session_state.etomidate_dose = etomidate_input
            st.session_state.ketamine_dose = ketamine_input
            st.session_state.midazolam_dose = midazolam_input
            st.session_state.thiopental_dose = thiopental_input
            st.session_state.atropine_indications = atropine_indications
            st.session_state.glycopyrrolate_indications = glycopyrrolate_indications

            # Debugging output after submission
            st.write("Input values updated:", st.session_state)

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Difficult Airway Evaluation"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Methods"  # Set next page
            st.rerun()




elif st.session_state.page == "Method":
    st.header("METHOD")

    # Dropdown for Method of Airway Management
    st.markdown("### Method: Begin NEW course if NEW method/device used")
    method_options = ["Select Method", "Oral", "Nasal", "LMA", "Oral to Oral", "Oral to Nasal", "Nasal to Oral", "Nasal to Nasal", "Tracheostomy to Oral"]

    if "selected_method" not in st.session_state:
        st.session_state.selected_method = method_options[0]

    selected_method = st.selectbox("Select Method:", method_options,
                                    index=method_options.index(st.session_state.selected_method))

    # Update the session state
    st.session_state.selected_method = selected_method

    # Multiselect for Airway Management Techniques and Medication Protocols
    st.markdown("### What airway management technique and/or their corresponding medication protocol was used during this course?")
    technique_options = [
        "Standard Sequence (administration of induction meds, PPV, then paralysis)",
        "Paralysis Only",
        "Rapid Sequence requiring positive pressure ventilation (PPV)",
        "Awake, topical",
        "Rapid Sequence without PPV (Classic RSI)",
        "No medications",
        "Sedation & Paralysis (Change of tube or subsequent courses)",
        "Surgical – Cricothyrotomy/Tracheostomy",
        "Sedation Only",
        "Others (Specify):"
    ]

    if "selected_techniques" not in st.session_state:
        st.session_state.selected_techniques = []

    selected_techniques = st.multiselect("Select Techniques:", 
                                          technique_options, 
                                          default=st.session_state.selected_techniques)

    # Update the session state
    st.session_state.selected_techniques = selected_techniques

    # Initialize "Others" specification in session state
    if "other_specification" not in st.session_state:
        st.session_state.other_specification = ""

    # If "Others" is selected, show an input box for specification
    if "Others (Specify):" in selected_techniques:
        other_specification = st.text_input("Please specify:", 
                                             value=st.session_state.other_specification)
        st.session_state.other_specification = other_specification  # Update here
    else:
        st.session_state.other_specification = ""  # Clear input if "Others" is not selected

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Medications"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Method Details"  # Set next page (update this to your actual next page)
            st.rerun()



# Main application logic based on the current page
elif st.session_state.page == "Method Details":
    st.header("METHOD DETAILS")
    
    if "selected_oxygen" not in st.session_state:
        st.session_state.selected_oxygen = "Select if Oxygen was Provided DURING any TI attempts for this course"
    if "oxygen_explanation" not in st.session_state:
        st.session_state.oxygen_explanation = ""
    if "selected_methods" not in st.session_state:
        st.session_state.selected_methods = []
    if "liter_flow" not in st.session_state:
        st.session_state.liter_flow = {}
    if "fio2" not in st.session_state:
        st.session_state.fio2 = {}
    
    # Question about Oxygen provision
    st.markdown("### 1. Was Oxygen provided DURING any TI attempts for this course?")
    oxygen_options = [
        "Select if Oxygen was Provided DURING any TI attempts for this course",
        "YES", 
        "NO", 
        "ATTEMPTED but not done (explain on last page)"
    ]

    selected_oxygen = st.selectbox("Select an option:", oxygen_options, index=oxygen_options.index(st.session_state.selected_oxygen))
    st.session_state.selected_oxygen = selected_oxygen

    # Conditional input for explanation if "ATTEMPTED but not done" is selected
    if selected_oxygen == "ATTEMPTED but not done (explain on last page)":
        explanation = st.text_area("Please explain:", value=st.session_state.oxygen_explanation)
        st.session_state.oxygen_explanation = explanation  # Save explanation to session state

    # Show multiselect if "YES" is selected
    if selected_oxygen == "YES":
        st.markdown("### If Yes, how was the oxygen provided?")
        methods_options = [
            "NC without nasal airway",
            "NC with nasal airway",
            "Oral airway with oxygen port",
            "Through LMA",
            "HFNC",
            "NIV with nasal prong interface – provide PEEP/PIP",
            "Other (device, FiO2, Setting)"
        ]

        # Multiselect for oxygen provision methods
        selected_methods = st.multiselect("Select methods:", methods_options, default=st.session_state.selected_methods)
        st.session_state.selected_methods = selected_methods  # Save selected methods to session state

        # Create a header for the columns
        cols = st.columns(3)  # Create three columns
        with cols[0]:
            st.markdown("**METHOD**")
        with cols[1]:
            st.markdown("**LITER FLOW**")
        with cols[2]:
            st.markdown("**FIO2**")

        # Input for Liter Flow and FiO2 for each selected method
        for method in selected_methods:
            # Create unique keys for Liter Flow and FiO2
            liter_flow_key = f"liter_flow_{method.replace(' ', '_')}"
            fio2_key = f"fio2_{method.replace(' ', '_')}"

            # Initialize if not present
            if liter_flow_key not in st.session_state.liter_flow:
                st.session_state.liter_flow[liter_flow_key] = ""
            if fio2_key not in st.session_state.fio2:
                st.session_state.fio2[fio2_key] = ""

            # Create columns for each method input
            cols = st.columns(3)  # Create three columns

            with cols[0]:
                st.markdown("")
                st.markdown("")
                st.markdown(f"**{method}**")  # Method name

            with cols[1]:
                # Liter Flow input
                #liter_flow = st.text_input(f"Liter Flow for {method}:", value=st.session_state.liter_flow[liter_flow_key], key=liter_flow_key)
                liter_flow = st.text_input("", value=st.session_state.liter_flow[liter_flow_key], key=liter_flow_key)
                st.session_state.liter_flow[liter_flow_key] = liter_flow

            with cols[2]:
                # FiO2 input
                #fio2 = st.text_input(f"FiO2 for {method}:", value=st.session_state.fio2[fio2_key], key=fio2_key)
                fio2 = st.text_input("", value=st.session_state.fio2[fio2_key], key=fio2_key)
                st.session_state.fio2[fio2_key] = fio2

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Method"  # Update this to your actual previous page
            st.rerun()  # Refresh the app to apply changes

    with col2:
        if st.button("Next"):
            st.session_state.page = "Method Details II"  # Update this to your actual next page
            st.rerun()  # Refresh the app to apply changes


elif st.session_state.page == "Method Details II":
    st.header("METHOD DETAILS II")
    # Add additional content for Method Details II here


    # Device Selection (Dropdown)
    st.markdown("### Device (Check only ONE) Begin NEW course if NEW method / device used.")
    devices = [
        "Select a Device",
        "Laryngoscope",
        "Fiber optic-flex",
        "LMA (Laryngeal mask airway) only",
        "ET tube via trach-stoma",
        "Intubation through LMA",
        "Surgical airway – Percutaneous/Cricothyrotomy (Describe)",
        "Video laryngoscope - Unguided (e.g. Glidescope)",
        "Video laryngoscope – CMAC",
        "View FOR INTUBATOR: Direct / Indirect",
        "Other (please describe):"
    ]

    if "selected_device" not in st.session_state:
        st.session_state.selected_device = devices[0]  # Default to "Select a Device"

    selected_device = st.selectbox("Select device:", devices, index=devices.index(st.session_state.selected_device))
    st.session_state.selected_device = selected_device  # Save selection

    # Tracheal Intubation Confirmation
    st.markdown("### Tracheal Intubation Confirmation (Check ALL that apply)")
    confirmation_options = [
        "Adequate and equal chest rise",
        "Exhaled CO2 – colorimetric",
        "Appropriate breath sounds heard (Auscultation)",
        "Chest X-ray",
        "Humidity seen in endotracheal tube",
        "Second independent laryngoscopy",
        "Exhaled CO2 – capnography",
        "Others:"
    ]

    if "selected_confirmation" not in st.session_state:
        st.session_state.selected_confirmation = []

    selected_confirmation = st.multiselect("Select confirmation methods:", confirmation_options, default=st.session_state.selected_confirmation)
    st.session_state.selected_confirmation = selected_confirmation  # Save selection

    image_path = "image.png"
    st.markdown("### Glottic Exposure During Intubation (Check only ONE):")
    st.image(image_path, caption="Visual Reference for Glottic Exposure", use_column_width=True)

    glottic_exposure_options = [
        "Select an option",
        "I = Visualized entire vocal cords",
        "II = Visualized part of cords",
        "III = Visualized epiglottis only",
        "IV = Non visualized epiglottis",
        "V = Not Applicable (e.g. blind nasotracheal)"
    ]

    if "selected_glottic_exposure" not in st.session_state:
        st.session_state.selected_glottic_exposure = glottic_exposure_options[0]  # Default to "Select an option"

    selected_glottic_exposure = st.selectbox("Select glottic exposure:", glottic_exposure_options, index=glottic_exposure_options.index(st.session_state.selected_glottic_exposure))
    st.session_state.selected_glottic_exposure = selected_glottic_exposure  # Save selection

    # Events for Tracheal Intubation
    st.markdown("### Tracheal Intubation Associated Events (Check ALL that apply):")
    events = [
        "NONE",
        "Cardiac arrest – patient died",
        "Cardiac arrest – patient survived",
        "Main stem intubation",
        "Esophageal intubation, immediate recognition",
        "Esophageal intubation, delayed recognition",
        "Vomit with aspiration",
        "Vomit but No aspiration",
        "Hypotension, needs intervention (fluids/pressors)",
        "Hypertension, requiring therapy",
        "Epistaxis",
        "Dental trauma",
        "Lip trauma",
        "Laryngospasm",
        "Malignant hyperthermia",
        "Medication error",
        "Pneumothorax / pneumomediastinum",
        "Direct airway injury",
        "Dysrhythmia (includes Bradycardia<60/min)",
        "Pain/Agitation, req’d additional meds AND delay in intubation",
        "Other (Please describe):"
    ]

    if "selected_events" not in st.session_state:
        st.session_state.selected_events = []

    selected_events = st.multiselect("Select events associated with tracheal intubation:", events, default=st.session_state.selected_events)
    st.session_state.selected_events = selected_events  # Save selection

    # Description for "Other" option
    if "Other (Please describe):" in selected_events:
        if "other_event_description" not in st.session_state:
            st.session_state.other_event_description = ""
        other_description = st.text_input("Please describe:", value=st.session_state.other_event_description)
        st.session_state.other_event_description = other_description  # Save description

    # Pop-ups for selected events
    for event in selected_events:
        if event != "NONE":
            with st.expander(f"{event} - Link to Attempt #", expanded=True):
                attempt_key = f"{event}_attempt"
                if attempt_key not in st.session_state:
                    st.session_state[attempt_key] = "Attempt 1"  # Default value

                attempt = st.selectbox(f"Select Attempt # for {event}:", [f"Attempt {i}" for i in range(1, 9)], index=int(st.session_state[attempt_key].split()[1]) - 1, key=attempt_key)
                st.session_state[attempt_key] = attempt  # Save selection

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Method Details"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Monitoring of Vital Signs"  # Update this to your actual next page
            st.rerun()


if st.session_state.page == "Monitoring of Vital Signs":
    st.header("MONITORING OF VITAL SIGNS")
    st.subheader("Pulse Oximetry (%):")

    # Creating two columns
    cols = st.columns(2)

    # Highest Value Input
    if "highest_value" not in st.session_state:
        st.session_state.highest_value = ""  # Initialize if not present

    with cols[0]:
        highest_value = st.text_input("Highest Value prior to intubation:", value=st.session_state.highest_value)
        st.session_state.highest_value = highest_value  # Save input value

    # Lowest Value Input
    if "lowest_value" not in st.session_state:
        st.session_state.lowest_value = ""  # Initialize if not present

    with cols[1]:
        lowest_value = st.text_input("Lowest value during intubation:", value=st.session_state.lowest_value)
        st.session_state.lowest_value = lowest_value  # Save input value

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Method Details II"  # Adjust to your previous page
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Course Success"
            st.rerun()

if st.session_state.page == "Course Success":
    st.header("COURSE SUCCESS")

    # Successful tracheal intubation/advanced airway management
    if "course_success" not in st.session_state:
        st.session_state.course_success = "Yes"  # Default value

    successful_intubation = st.selectbox(
        "Successful tracheal intubation/advanced airway management:", 
        ["Yes", "No"], 
        index=["Yes", "No"].index(st.session_state.course_success)
    )
    st.session_state.course_success = successful_intubation  # Save selection

    if successful_intubation == "No":
        st.markdown("If course failed, please explain briefly:")
        
        # Checkbox inputs
        st.checkbox("Cannot visualize vocal cords", value=st.session_state.get("cannot_visualize", False), key="cannot_visualize")
        st.checkbox("Cannot place device into trachea", value=st.session_state.get("cannot_place_device", False), key="cannot_place_device")
        st.checkbox("Unstable hemodynamics", value=st.session_state.get("unstable_hemodynamics", False), key="unstable_hemodynamics")
        
        # Other failure explanation
        if "other_failure" not in st.session_state:
            st.session_state.other_failure = ""  # Initialize if not present
        other_failure = st.text_input("Other (please explain):", value=st.session_state.other_failure)
        st.session_state.other_failure = other_failure  # Save input

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Monitoring of Vital Signs"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Disposition"
            st.rerun()

if st.session_state.page == "Disposition":
    st.header("DISPOSITION")

    # Disposition options
    disposition_options = [
        "Stay in PICU/NICU/CICU/ED",
        "Transferred to",
        "Died – due to failed airway management",
        "Died – other causes",
        "Other"
    ]

    if "disposition" not in st.session_state:
        st.session_state.disposition = disposition_options[0]  # Default value

    disposition = st.selectbox(
        "Disposition:", 
        disposition_options, 
        index=disposition_options.index(st.session_state.disposition)
    )
    st.session_state.disposition = disposition  # Save selection

    # Transferred to checkboxes
    if disposition == "Transferred to":
        st.checkbox("PICU", value=st.session_state.get("transferred_to_PICU", False), key="transferred_to_PICU")
        st.checkbox("NICU", value=st.session_state.get("transferred_to_NICU", False), key="transferred_to_NICU")
        st.checkbox("CICU", value=st.session_state.get("transferred_to_CICU", False), key="transferred_to_CICU")

    # Other disposition input
    if disposition == "Other":
        if "other_disposition" not in st.session_state:
            st.session_state.other_disposition = ""  # Initialize if not present
        other_disposition = st.text_input("Please specify:", value=st.session_state.other_disposition)
        st.session_state.other_disposition = other_disposition  # Save input
    else:
        st.session_state.other_disposition = ""  # Clear input if not "Other"

    # Other comments
    if "other_comments" not in st.session_state:
        st.session_state.other_comments = ""  # Initialize if not present
    other_comments = st.text_area("Please explain (e.g. higher dose of vecuronium, choice of drugs used):", value=st.session_state.other_comments)
    st.session_state.other_comments = other_comments  # Save input

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Course Success"
            st.rerun()

    with col2:
        if st.button("Submit"):
            st.session_state.page = "Summary"  # Change to your final page
            st.rerun()



