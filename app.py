import streamlit as st
import datetime
import json
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
from docx import Document
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib


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

st.title("NEAR4KIDS QI COLLECTION FORM")

# Initialize session state for page and user paragraph
if 'page' not in st.session_state:
    st.session_state.page = "Starting Page"  # Default page

if 'user_paragraph' not in st.session_state:
    st.session_state.user_paragraph = ""

if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

if 'glottic_exposure' not in st.session_state:
    st.session_state.glottic_exposure = "Select a Glottic Exposure"  # Default to "Select a Glottic Exposure"

if st.session_state.page == "Starting Page":
    # Text area for user input
    user_paragraph = st.text_area("Please enter a paragraph:", value=st.session_state.user_paragraph)

    # Navigation buttons
    col_prev, col_next = st.columns(2)

    with col_next:
        if st.button("Next"):
            st.session_state.user_paragraph = user_paragraph
            
            # Logic to check for grade inputs and assign glottic exposure
            if "grade 1" in user_paragraph.lower() or "grade i" in user_paragraph.lower():
                st.session_state.glottic_exposure = "I = Visualized entire vocal cords"
            elif "grade 2" in user_paragraph.lower() or "grade ii" in user_paragraph.lower():
                st.session_state.glottic_exposure = "II = Visualized part of cords"
            elif "grade 3" in user_paragraph.lower() or "grade iii" in user_paragraph.lower():
                st.session_state.glottic_exposure = "III = Visualized epiglottis only"
            elif "grade 4" in user_paragraph.lower() or "grade iv" in user_paragraph.lower():
                st.session_state.glottic_exposure = "IV = Non visualized epiglottis"
            elif "grade 5" in user_paragraph.lower() or "grade v" in user_paragraph.lower():
                st.session_state.glottic_exposure = "V = Not Applicable (e.g. blind nasotracheal)"

            # Extracting Date:
            date_part = None
            time_part = None
            performed_by = None
            attending_physician_present = "No"  # Default value

            if "Date:" in user_paragraph:
                date_section = user_paragraph.split("Date:")[1]
                if '.' in date_section:
                    date_part = date_section.split('.')[0].strip()
                else:
                    date_part = date_section.strip()

            # Extracting Date/ Time:
            if "Date/ Time:" in user_paragraph:
                datetime_part = user_paragraph.split("Date/ Time:")[1].strip()
                if datetime_part:
                    date_time = datetime_part.split()
                    if len(date_time) >= 2:
                        date_part = date_time[0]
                        time_part = date_time[1]

            # Extracting Performed by:
            if "Performed by:" in user_paragraph:
                performed_by_section = user_paragraph.split("Performed by:")[1]
                if '.' in performed_by_section:
                    performed_by = performed_by_section.split('.')[0].strip()
                else:
                    performed_by = performed_by_section.strip()

            # Extracting Present and supervised procedure:
            if "Present and supervised procedure:" in user_paragraph:
                attending_physician_present = "Yes"  # Set default to Yes
                physician_section = user_paragraph.split("Present and supervised procedure:")[1]
                if '.' in physician_section:
                    physician_name = physician_section.split('.')[0].strip()
                else:
                    physician_name = physician_section.strip()

            # Store extracted data in form_data
            st.session_state.form_data['date'] = date_part if date_part else None
            st.session_state.form_data['time'] = time_part if time_part else None
            st.session_state.form_data['form_completed_by'] = performed_by if performed_by else ''
            st.session_state.form_data['attending_physician_present'] = attending_physician_present
            
            st.session_state.page = "Encounter Information"  # Set next page
            st.rerun()


# Page Navigation
elif st.session_state.page == "Encounter Information":
    # Header for Encounter Information
    st.header("ENCOUNTER INFORMATION")
    st.subheader("Patient Information")

    # First line: Date, Time, Location
    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state.form_data['date'] = st.text_input(
            "Date:", 
            value=st.session_state.form_data.get('date', '')
        )
    
    with col2:
        st.session_state.form_data['time'] = st.text_input(
            "Time:", 
            value=st.session_state.form_data.get('time', '')
        )

    with col3:
        st.session_state.form_data['location'] = st.text_input(
            "Location:", 
            value=st.session_state.form_data.get('location', '')
        )

    # Second line: Patient Gender, Patient Dosing Weight
    col4, col5 = st.columns(2)
    with col4:
        st.session_state.form_data['patient_gender'] = st.selectbox(
            "Patient Gender:", 
            options=["Select Gender", "Male", "Female", "Other"], 
            index=["Select Gender", "Male", "Female", "Other"].index(st.session_state.form_data.get('patient_gender', 'Select Gender'))
        )
    with col5:
        st.session_state.form_data['dosing_weight'] = st.text_input(
            "Patient Dosing Weight (kg):", 
            value=st.session_state.form_data.get('dosing_weight', '')
        )

    # Diagnosis query
    st.write("AT THE TIME OF INTUBATION, did this patient have a suspected or confirmed diagnosis of an emerging epidemic/novel lung disease?")
    st.session_state.form_data['diagnosis'] = st.selectbox(
        "Select if patient has a suspected or confirmed diagnosis of an emerging epidemic/novel lung disease:", 
        options=["Select if patient has a suspected or confirmed diagnosis", "Yes", "No"], 
        index=["Select if patient has a suspected or confirmed diagnosis", "Yes", "No"].index(st.session_state.form_data.get('diagnosis', 'Select if patient has a suspected or confirmed diagnosis'))
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
            options=["Select if Family Member Present", "Yes", "No"], 
            index=["Select if Family Member Present", "Yes", "No"].index(st.session_state.form_data.get('family_member_present', 'Select if Family Member Present'))
        )
    with col9:
        st.session_state.form_data['attending_physician_present'] = st.selectbox(
            "Attending Physician Present:", 
            options=["Select if Attending Physician Present", "Yes", "No"], 
            index=["Select if Attending Physician Present", "Yes", "No"].index(st.session_state.form_data.get('attending_physician_present', 'Select if Attending Physician Present'))
        )

    st.session_state.form_data['airway_bundle'] = st.selectbox(
            "Airway Bundle/Pink Sheet Completed – Front AND Back:", 
            options=["Select if Airway Bundle/Pink Sheet Completed", "Yes", "No"], 
            index=["Select if Airway Bundle/Pink Sheet Completed", "Yes", "No"].index(st.session_state.form_data.get('airway_bundle', 'Select if Airway Bundle/Pink Sheet Completed'))
        )

    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Starting Page"
            st.rerun()

    with col_next:
        # Only proceed if button is clicked
        if st.button("Next"):
            # Validation check for required fields
            missing_fields = []
            if st.session_state.form_data['patient_gender'] == "Select Gender":
                missing_fields.append("Patient Gender")
            if st.session_state.form_data['dosing_weight'] == "":
                missing_fields.append("Patient Dosing Weight")
            if st.session_state.form_data['time'] == "":
                missing_fields.append("Time")
            if st.session_state.form_data['location'] == "":
                missing_fields.append("Location")
            if st.session_state.form_data['pager_number'] == "":
                missing_fields.append("Pager Number")
            if st.session_state.form_data['diagnosis'] == "Select if patient has a suspected or confirmed diagnosis":
                missing_fields.append("Diagnosis")
            if st.session_state.form_data['family_member_present'] == "Select if Family Member Present":
                missing_fields.append("Family Member Present")
            if st.session_state.form_data['attending_physician_present'] == "Select if Attending Physician Present":
                missing_fields.append("Attending Physician Present")
            if st.session_state.form_data['airway_bundle'] == "Select if Airway Bundle/Pink Sheet Completed":
                missing_fields.append("Airway Bundle/Pink Sheet Present")

            if missing_fields:
                st.warning(f"Please fill in the following: {', '.join(missing_fields)}")
            else:
                st.session_state.page = "Indications"  # Set next page
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
    else:
        # Reset dosages and indications if no drugs are used
        st.session_state.atropine_dose = ""
        st.session_state.glycopyrrolate_dose = ""
        st.session_state.fentanyl_dose = ""
        st.session_state.lidocaine_dose = ""
        st.session_state.vecuronium_dose = ""
        st.session_state.rocuronium_dose = ""
        st.session_state.succinylcholine_dose = ""
        st.session_state.pancuronium_dose = ""
        st.session_state.cisatracuronium_dose = ""
        st.session_state.propofol_dose = ""
        st.session_state.etomidate_dose = ""
        st.session_state.ketamine_dose = ""
        st.session_state.midazolam_dose = ""
        st.session_state.thiopental_dose = ""
        st.session_state.atropine_indications = []
        st.session_state.glycopyrrolate_indications = []

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous"):
            st.session_state.page = "Difficult Airway Evaluation"
            st.rerun()

    with col2:
        if st.button("Next"):
            # Update session state when moving to the next page
            if no_drugs == "DRUGS USED":
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

            st.session_state.page = "Method"  # Set next page
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
    #if selected_oxygen == "ATTEMPTED but not done (explain on last page)":
    #    explanation = st.text_area("Please explain:", value=st.session_state.oxygen_explanation)
    #    st.session_state.oxygen_explanation = explanation  # Save explanation to session state

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

    selected_device = st.selectbox("Select Device:", devices, index=devices.index(st.session_state.selected_device))
    st.session_state.selected_device = selected_device  # Save selection

    # Text input for 'Other' device description
    if selected_device == "Other (please describe):":
        if "other_device_description" not in st.session_state:
            st.session_state.other_device_description = ""
        other_device_description = st.text_input("Please describe the Other Device:", value=st.session_state.other_device_description)
        st.session_state.other_device_description = other_device_description  # Save description

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

    # Text input for 'Other' confirmation description
    if "Others:" in selected_confirmation:
        if "other_confirmation_description" not in st.session_state:
            st.session_state.other_confirmation_description = ""
        other_confirmation_description = st.text_input("Please describe the Other Confirmation Method:", value=st.session_state.other_confirmation_description)
        st.session_state.other_confirmation_description = other_confirmation_description  # Save description

    st.markdown("### Glottic Exposure During Intubation [Check only ONE]:")
    st.image("image.png", caption="Glottic Exposure Diagram", use_column_width=True)  # Add the image here
    glottic_options = [
        "Select a Glottic Exposure",
        "I = Visualized entire vocal cords",
        "II = Visualized part of cords",
        "III = Visualized epiglottis only",
        "IV = Non visualized epiglottis",
        "V = Not Applicable (e.g. blind nasotracheal)"
    ]
    
    glottic_exposure = st.selectbox("Select Glottic Exposure:", glottic_options, index=glottic_options.index(st.session_state.glottic_exposure))
    st.session_state.glottic_exposure = glottic_exposure

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

    # Text input for 'Other' event description
    if "Other (Please describe):" in selected_events:
        if "other_event_description" not in st.session_state:
            st.session_state.other_event_description = ""
        other_event_description = st.text_input("Please describe the Other Tracheal Intubation Event:", value=st.session_state.other_event_description)
        st.session_state.other_event_description = other_event_description  # Save description

    # Initialize attempt mapping if not already done
    if "attempt_mapping" not in st.session_state:
        st.session_state.attempt_mapping = {i: [] for i in range(1, 9)}  # Create mapping for attempts 1 to 8
    
    # Popup for linking events to attempt numbers
    if selected_events:
        event_to_link = st.selectbox("Select an event to link:", selected_events)
        attempt_number = st.selectbox("Select Attempt Number:", list(range(1, 9)))
        
        if st.button("Link Event to Attempt"):
            if event_to_link != "NONE":  # Ensure the selected event is valid
                st.session_state.attempt_mapping[attempt_number].append(event_to_link)
                st.success(f"Linked '{event_to_link}' to Attempt {attempt_number}!")
            else:
                st.warning("No valid event selected.")
    
    # Display linked events
    st.markdown("### Linked Events:")
    for attempt_number, events in st.session_state.attempt_mapping.items():
        if events:
            st.write(f"Attempt {attempt_number}: {', '.join(events)}")

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

    # Initialize checkboxes for failure explanations
    if "cannot_visualize" not in st.session_state:
        st.session_state.cannot_visualize = False
    if "cannot_place_device" not in st.session_state:
        st.session_state.cannot_place_device = False
    if "unstable_hemodynamics" not in st.session_state:
        st.session_state.unstable_hemodynamics = False

    # Successful tracheal intubation/advanced airway management
    if "course_success" not in st.session_state:
        st.session_state.course_success = "Yes"  # Default value

    successful_intubation = st.selectbox(
        "Successful tracheal intubation/advanced airway management:", 
        ["Yes", "No"], 
        index=["Yes", "No"].index(st.session_state.course_success)
    )
    st.session_state.course_success = successful_intubation  # Save selection

    # Initialize other_failure variable
    if "other_failure" not in st.session_state:
        st.session_state.other_failure = ""  # Initialize if not present
    other_failure = st.session_state.other_failure  # Get current value

    # Initialize variables for checkboxes only if the course failed
    if successful_intubation == "No":
        st.markdown("If course failed, please explain briefly:")
        
        cannot_visualize = st.checkbox("Cannot visualize vocal cords", value=st.session_state.cannot_visualize)
        cannot_place_device = st.checkbox("Cannot place device into trachea", value=st.session_state.cannot_place_device)
        unstable_hemodynamics = st.checkbox("Unstable hemodynamics", value=st.session_state.unstable_hemodynamics)

        # Other failure explanation input
        other_failure = st.text_input("Other (please explain):", value=other_failure)
    else:
        # Ensure variables are defined even if not used
        cannot_visualize = st.session_state.cannot_visualize
        cannot_place_device = st.session_state.cannot_place_device
        unstable_hemodynamics = st.session_state.unstable_hemodynamics

    # Navigation buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Previous"):
            # Save checkbox states when moving to the previous page
            st.session_state.cannot_visualize = cannot_visualize
            st.session_state.cannot_place_device = cannot_place_device
            st.session_state.unstable_hemodynamics = unstable_hemodynamics
            st.session_state.page = "Monitoring of Vital Signs"
            st.rerun()

    with col2:
        if st.button("Next"):
            # Save checkbox states when moving to the next page
            st.session_state.cannot_visualize = cannot_visualize
            st.session_state.cannot_place_device = cannot_place_device
            st.session_state.unstable_hemodynamics = unstable_hemodynamics
            
            # Save the other failure explanation
            st.session_state.other_failure = other_failure

            # Navigate to the next page
            st.session_state.page = "Disposition"
            st.rerun()

elif st.session_state.page == "Disposition":
    st.header("DISPOSITION")

    # Disposition options
    disposition_options = [
        "Stay in PICU/NICU/CICU/ED",
        "Transferred to",
        "Died – due to failed airway management",
        "Died – other causes",
        "Other"
    ]

    # Initialize disposition in session state if not present
    if "disposition" not in st.session_state:
        st.session_state.disposition = disposition_options[0]  # Default value

    disposition = st.selectbox(
        "Disposition:", 
        disposition_options, 
        index=disposition_options.index(st.session_state.disposition)
    )
    st.session_state.disposition = disposition  # Save selection

    # Initialize transferred_to checkboxes if not already done
    if "transferred_to_PICU" not in st.session_state:
        st.session_state.transferred_to_PICU = False
    if "transferred_to_NICU" not in st.session_state:
        st.session_state.transferred_to_NICU = False
    if "transferred_to_CICU" not in st.session_state:
        st.session_state.transferred_to_CICU = False

    # Checkboxes (only if "Transferred to" is selected)
    transferred_to_PICU = st.session_state.transferred_to_PICU if disposition == "Transferred to" else False
    transferred_to_NICU = st.session_state.transferred_to_NICU if disposition == "Transferred to" else False
    transferred_to_CICU = st.session_state.transferred_to_CICU if disposition == "Transferred to" else False

    if disposition == "Transferred to":
        transferred_to_PICU = st.checkbox("PICU", value=st.session_state.transferred_to_PICU)
        transferred_to_NICU = st.checkbox("NICU", value=st.session_state.transferred_to_NICU)
        transferred_to_CICU = st.checkbox("CICU", value=st.session_state.transferred_to_CICU)
    else:
        # Reset checkboxes if disposition is not "Transferred to"
        st.session_state.transferred_to_PICU = False
        st.session_state.transferred_to_NICU = False
        st.session_state.transferred_to_CICU = False

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
            # Save checkbox states when moving to the previous page
            st.session_state.transferred_to_PICU = transferred_to_PICU
            st.session_state.transferred_to_NICU = transferred_to_NICU
            st.session_state.transferred_to_CICU = transferred_to_CICU
            st.session_state.page = "Course Success"
            st.rerun()

    with col2:
        if st.button("Next"):
            # Save checkbox states when moving to the next page
            st.session_state.transferred_to_PICU = transferred_to_PICU
            st.session_state.transferred_to_NICU = transferred_to_NICU
            st.session_state.transferred_to_CICU = transferred_to_CICU
            
            # Navigate to the next page
            st.session_state.page = "Summary"  # Change to your final page
            st.rerun()

# Function to send email with attachment
def send_email_with_attachment(to_emails, subject, body, file_path):
    from_email = st.secrets["general"]["email"]
    password = st.secrets["general"]["email_password"]

    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)  # Join multiple email addresses
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'html'))

    # Attach the Word document
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={file_path.split("/")[-1]}')
        msg.attach(part)

    # Send the email using SMTP with SSL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
            st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")
        
if 'firebase_initialized' not in st.session_state:
    firebase_key = st.secrets["FIREBASE_KEY"]
    cred = credentials.Certificate(json.loads(firebase_key))

    try:
        firebase_admin.initialize_app(cred)
        st.session_state.firebase_initialized = True
    except ValueError as e:
        if "already exists" in str(e):
            pass  # App is already initialized
        else:
            st.error(f"Failed to initialize Firebase: {str(e)}")

# Access Firestore
if 'db' not in st.session_state:
    try:
        st.session_state.db = firestore.client()
    except Exception as e:
        st.error(f"Failed to connect to Firestore: {str(e)}")

def create_word_doc(template_path, data):
    doc = Document(template_path)

    # Define your placeholders
    placeholders = {
        '{date_placeholder}': data['date'],
        '{time_placeholder}': data['time'],
        '{location_placeholder}:data['location'],
        # Add more placeholders as needed...
    }

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for placeholder, value in placeholders.items():
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)

    # Replace placeholders in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        for placeholder, value in placeholders.items():
                            if placeholder in run.text:
                                run.text = run.text.replace(placeholder, value)

    output_path = 'n4k_dcf.docx'  # Change this to your desired output path
    doc.save(output_path)

    return output_path


# Summary Page Logic
if st.session_state.page == "Summary":
    st.header("SUMMARY")

    user_email = st.text_input("Enter your email address (optional):", value="", key="user_email_input")

    if 'doc_file' not in st.session_state:
        st.session_state.doc_file = None

    col_prev, col_submit = st.columns(2)

    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Disposition"
            st.rerun()

    with col_submit:
        if st.button("Submit"):
            document_data = {
                'date': st.session_state.form_data.get('date', ''),
                'time': st.session_state.form_data.get('time', ''),
            }
            st.write(st.session_state.form_data['date'])
            template_path = 'nqf.docx' 

            try:
                st.session_state.doc_file = create_word_doc(template_path, document_data)
                st.success("Document created successfully!")
                
                # Define subject and message for email
                subject = "White Form Submission"
                message = f"Here is the White Form.<br><br>Date: {document_data['date']}<br>Time: {document_data['time']}<br>Form Completed By:"

                # Prepare the email recipients
                to_emails = [st.secrets["general"]["email_r"]]  # Designated email
                if user_email:  # Add user's email if provided
                    to_emails.append(user_email)

                # Prepare data to be saved in Firestore
                email_data = {
                    "to": to_emails,
                    "message": {
                        "subject": subject,
                    },
                    "date": document_data['date'],
                }

                # Firestore upload
                db = st.session_state.db
                db.collection("N4KFORMW").add(document_data)
                st.success("Form submitted successfully!")

                # Send email with attachment
                #send_email_with_attachment(to_emails, subject, message, st.session_state.doc_file)

                with open(st.session_state.doc_file, 'rb') as f:
                    st.download_button(
                        label="Download Word Document",
                        data=f,
                        file_name=st.session_state.doc_file.split("/")[-1],
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")




