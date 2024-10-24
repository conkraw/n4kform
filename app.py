import streamlit as st
from flask import Flask, request
import threading

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
            'who_intubated': None,
            'discipline': None,
            'pgy_level': None,
            'ett_size': None,
            'ett_type': None,
            'cricoid_prior': None,
            'cricoid_during': None,
            'attempt_successful': None,
        } for i in range(1, 9)}

    # Define the row headers
    row_headers = [
        "Attempts for this COURSE",
        "Who intubated (Fellow, Resident, etc)",
        "Discipline (ICU, ENT, Surgery, etc)",
        "PGY level (3rd year resident = PL3, 1st year fellow = PL4,  NP=yrs as NP, etc.)",
        "ETT (or LMA) Size",
        "ETT type: cuffed/uncuffed/ NA",
        "Immediately prior to this attempt was cricoid pressure/external laryngeal manipulation provided?",
        "During this attempt, was cricoid pressure/external laryngeal manipulation provided?",
        "Attempt Successful: Yes/No"
    ]

    # Define attempt numbers
    attempt_numbers = range(1, 9)

    # Create the table-like layout
    with st.form("course_information_form"):  # Start the form
        for row_header in row_headers:
            cols = st.columns(len(attempt_numbers) + 1)  # Create extra column for headers
            with cols[0]:  # Column for row headers
                reset_input(row_header, f"header_{row_header}")   # No default value for headers

            for attempt in attempt_numbers:
                with cols[attempt]:  # Adjust for 1-based indexing
                    if row_header == "Attempts for this COURSE":
                        centered_input(str(attempt), f"attempt_course_{attempt}", width='50px', height='40px') 
                    elif row_header == "Who intubated (Fellow, Resident, etc)":
                        st.session_state.attempts[f'Attempt {attempt}']['who_intubated'] = custom_input(
                            f'who_intubated_{attempt}'
                        )
                    elif row_header == "Discipline (ICU, ENT, Surgery, etc)":
                        st.session_state.attempts[f'Attempt {attempt}']['discipline'] = custom_input(
                            f'discipline_{attempt}'
                        )
                    elif row_header == "PGY level (3rd year resident = PL3, 1st year fellow = PL4,  NP=yrs as NP, etc.)":
                        st.session_state.attempts[f'Attempt {attempt}']['pgy_level'] = custom_input(
                            f'pgy_level_{attempt}'
                        )
                    elif row_header == "ETT (or LMA) Size":
                        st.session_state.attempts[f'Attempt {attempt}']['ett_size'] = custom_input(
                            f'ett_size_{attempt}'
                        )
                    elif row_header == "ETT type: cuffed/uncuffed/ NA":
                        st.session_state.attempts[f'Attempt {attempt}']['ett_type'] = custom_input(
                            f'ett_type_{attempt}'
                        )
                    elif row_header == "Immediately prior to this attempt was cricoid pressure/external laryngeal manipulation provided?":
                        st.session_state.attempts[f'Attempt {attempt}']['cricoid_prior'] = custom_input(
                            f'cricoid_prior_{attempt}'
                        )
                    elif row_header == "During this attempt, was cricoid pressure/external laryngeal manipulation provided?":
                        st.session_state.attempts[f'Attempt {attempt}']['cricoid_during'] = custom_input(
                            f'cricoid_during_{attempt}'
                        )
                    elif row_header == "Attempt Successful: Yes/No":
                        st.session_state.attempts[f'Attempt {attempt}']['attempt_successful'] = custom_input(
                            f'attempt_successful_{attempt}'
                        )

        # Ensure the session state is initialized for all relevant keys first
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
        
        # Initialize session state for each question
        for idx, (_, options) in enumerate(questions):
            key = f"evaluation_{idx}"
            if key not in st.session_state:
                st.session_state[key] = options[0]  # Set default value
        
        # Now create the layout
        st.markdown("### Difficult Airway Evaluations (Choose one in each category):")
        
        for idx, (question, options) in enumerate(questions):
            cols = st.columns([4, 1])
            
            with cols[0]:
                question_box(f"{idx + 1}. {question}")
                
            with cols[1]:
                # Create selectbox with options
                selected_option = st.selectbox(
                    "",
                    options=options,
                    index=options.index(st.session_state[f"evaluation_{idx}"]),
                    key=f"evaluation_{idx}"  # Unique key for each selectbox
                )

        # Create a select box for options
        st.markdown("### Difficult to Bag/Mask Ventilate? (Select ONE only)")
        options_bag = ["Yes", "No", "Not applicable (bag-mask ventilation not given)"]
        selected_bag = st.selectbox("", options_bag, key="difficult_to_bag")
        
        # Known cyanotic heart disease (R to L shunt)
        st.markdown("### Known cyanotic heart disease (R to L shunt)?  (Select ONE only)")
        options_cyanotic = ["Yes", "No"]
        selected_cyanotic = st.selectbox("", options_cyanotic, key="cyanotic")

        # Submit button for the form
        submitted = st.form_submit_button("Next")
        if submitted:
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

    # Select box for drugs used
    no_drugs = st.selectbox("Have any drugs been used?", ["NO DRUGS USED", "DRUGS USED"], index=0)

    if no_drugs == "NO DRUGS USED":
        st.markdown("If no drugs are used, please proceed to the next section.")
    else:
        # Create columns for dosages
        cols = st.columns(3)

        # Pretreatment Dosage
        with cols[0]:
            st.markdown("### Pretreatment Dosage")
            st.text_input("Atropine (mg)", key="pretreatment_atropine")
            st.text_input("Glycopyrrolate (mcg)", key="pretreatment_glycopyrrolate")
            st.text_input("Fentanyl (mcg)", key="pretreatment_fentanyl")
            st.text_input("Lidocaine (mg)", key="pretreatment_lidocaine")
            st.text_input("Vecuronium (mg)", key="pretreatment_vecuronium")
            st.text_input("Others", key="pretreatment_others")

        # Paralysis Dosage
        with cols[1]:
            st.markdown("### Paralysis Dosage")
            st.text_input("Rocuronium (mg)", key="paralysis_rocuronium")
            st.text_input("Succinylcholine (mg)", key="paralysis_succinylcholine")
            st.text_input("Vecuronium (mg)", key="paralysis_vecuronium")
            st.text_input("Pancuronium (mg)", key="paralysis_pancuronium")
            st.text_input("Cisatracuronium (mg)", key="paralysis_cisatracuronium")
            st.text_input("Others", key="paralysis_others")

        # Induction Dosage
        with cols[2]:
            st.markdown("### Induction Dosage")
            st.text_input("Propofol (mg)", key="induction_propofol")
            st.text_input("Etomidate (mg)", key="induction_etomidate")
            st.text_input("Ketamine (mg)", key="induction_ketamine")
            st.text_input("Midazolam (mg)", key="induction_midazolam")
            st.text_input("Thiopental (mg)", key="induction_thiopental")
            st.text_input("Others", key="induction_others")

        # Multi-select for indications
        st.markdown("### Indications")
        atropine_indication = st.multiselect(
            "Atropine Indication:",
            ["Premed for TI", "Treatment of Bradycardia"],
            key="atropine_indication"
        )

        glycopyrrolate_indication = st.multiselect(
            "Glycopyrrolate Indication:",
            ["Premed for TI", "Treatment of Bradycardia"],
            key="glycopyrrolate_indication"
        )

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Course Information"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Method"  # Set next page
            st.rerun()

elif st.session_state.page == "Method":
    st.header("METHOD")

    # Dropdown for Method of Airway Management
    st.markdown("### Method: Begin NEW course if NEW method/device used")
    method_options = [
        "Oral", "Nasal", "LMA", "Oral to Oral",
        "Oral to Nasal", "Nasal to Oral", "Nasal to Nasal", "Tracheostomy to Oral"
    ]
    selected_method = st.selectbox("Select Method:", method_options, key="airway_method")

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
    selected_techniques = st.multiselect("Select Techniques:", technique_options, key="airway_techniques")

    # If "Others" is selected, show an input box for specification
    if "Others (Specify):" in selected_techniques:
        other_specification = st.text_input("Please specify:", key="other_specification")

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

import streamlit as st

# Page for Method Details
if st.session_state.page == "Method Details":
    st.header("METHOD DETAILS")

    # Question about Oxygen provision
    st.markdown("### 1. Was Oxygen provided DURING any TI attempts for this course?")
    oxygen_options = ["YES", "NO", "ATTEMPTED but not done (explain on last page)"]
    selected_oxygen = st.selectbox("Select an option:", oxygen_options, key="oxygen_provided")

    # Conditional input for explanation if "ATTEMPTED but not done" is selected
    if selected_oxygen == "ATTEMPTED but not done (explain on last page)":
        explanation = st.text_area("Please explain:", key="oxygen_explanation")

    # Additional section if "YES" is selected
    if selected_oxygen == "YES":
        st.markdown("### If Yes, How was the oxygen provided:")

        # Multi-select for oxygen provision methods
        options = [
            "NC without nasal airway",
            "NC with nasal airway",
            "Oral airway with oxygen port",
            "Through LMA",
            "HFNC",
            "NIV with nasal prong interface - provide PEEP/PIP",
            "Other (device, FIO2, setting)"
        ]
        selected_methods = st.multiselect("Select methods:", options)

        # Display Liter Flow and FIO2 inputs for each selected method
        if selected_methods:
            st.write("#### Oxygen Provision Details")
            cols = st.columns(4)  # Create four columns

            with cols[0]:
                st.markdown("**METHOD**")
            with cols[1]:
                st.markdown("**LITER FLOW**")
            with cols[2]:
                st.markdown("**FIO2**")

            for method in selected_methods:
                cols = st.columns(4)  # Create a row for each method

                with cols[0]:
                    st.markdown("")
                    st.markdown("")
                    st.markdown(f"**{method}**")
                
                with cols[1]:
                    liter_flow = st.text_input("", key=f"liter_flow_{method.replace(' ', '_')}")
                
                with cols[2]:
                    fio2 = st.text_input("", key=f"fio2_{method.replace(' ', '_')}")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Method"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Method Details II"  # Update this to your actual next page
            st.rerun()



elif st.session_state.page == "Method Details II":
    st.header("METHOD DETAILS II")

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
    selected_device = st.selectbox("Select device:", devices)

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
    selected_confirmation = st.multiselect("Select confirmation methods:", confirmation_options)

    st.markdown("### Glottic Exposure During Intubation (Check only ONE):")
    glottic_exposure_options = [
        "Select an option",
        "I = Visualized entire vocal cords",
        "II = Visualized part of cords",
        "III = Visualized epiglottis only",
        "IV = Non visualized epiglottis",
        "V = Not Applicable (e.g. blind nasotracheal)"
    ]
    selected_glottic_exposure = st.selectbox("Select glottic exposure:", glottic_exposure_options)

    # Events for Tracheal Intubation
    st.markdown("### Tracheal Intubation Associated Events (Check ALL that apply):")
    
    # List of events
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
    
    # Multi-select for events
    selected_events = st.multiselect("Select events associated with tracheal intubation:", events)
    
    # Description for "Other" option
    if "Other (Please describe):" in selected_events:
        other_description = st.text_input("Please describe:", key="other_event_description")
    
    # Pop-ups for selected events
    for event in selected_events:
        if event != "NONE":
            with st.expander(f"{event} - Link to Attempt #", expanded=True):
                attempt = st.selectbox(f"Select Attempt # for {event}:", [f"Attempt {i}" for i in range(1, 9)], key=f"{event}_attempt")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Method Details II"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.page = "Monitoring of Vital Signs"  # Update this to your actual next page
            st.rerun()


if st.session_state.page == "Monitoring of Vital Signs":
    st.header("MONITORING OF VITAL SIGNS")
    st.subheader("Pulse Oximetry:")

    # Creating four columns
    cols = st.columns(2)

    with cols[0]:
        highest_value = st.text_input("Highest Value prior to intubation:", key="highest_value")

    with cols[1]:
        lowest_value = st.text_input("Lowest value during intubation:", key="lowest_value")


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

    successful_intubation = st.selectbox("Successful tracheal intubation/advanced airway management:", ["Yes", "No"], key="course_success")

    if successful_intubation == "No":
        st.markdown("If course failed, please explain briefly:")
        st.checkbox("Cannot visualize vocal cords", key="cannot_visualize")
        st.checkbox("Cannot place device into trachea", key="cannot_place_device")
        st.checkbox("Unstable hemodynamics", key="unstable_hemodynamics")
        other_failure = st.text_input("Other (please explain):", key="other_failure")

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

    disposition = st.selectbox("Disposition:", ["Stay in PICU/NICU/CICU/ED", "Transferred to", "Died – due to failed airway management", "Died – other causes"], key="disposition")

    if disposition == "Transferred to":
        st.checkbox("PICU", key="transferred_to_PICU")
        st.checkbox("NICU", key="transferred_to_NICU")
        st.checkbox("CICU", key="transferred_to_CICU")
    
    other_disposition = st.text_input("Others (Specify):", key="other_disposition")

    st.markdown("### Other Comments:")
    other_comments = st.text_area("Please explain (e.g. higher dose of vecuronium, choice of drugs used):", key="other_comments")

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


