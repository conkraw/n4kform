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
import pandas as pd 
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
import uuid

st.set_page_config(layout="wide")

def set_need_appearances_writer(writer: PdfFileWriter):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

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

# Initialize session state for page and form data
if 'page' not in st.session_state:
    st.session_state.page = "Encounter Information"  # Directly start with the Encounter Information page

if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

if 'glottic_exposure' not in st.session_state:
    st.session_state.glottic_exposure = "Select a Glottic Exposure"  # Default to "Select a Glottic Exposure"

# Page: Encounter Information
if st.session_state.page == "Encounter Information":
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

    if 'diagnostic_category' not in st.session_state.form_data:
        st.session_state.form_data['diagnostic_category'] = []
    
    # Update the session state with selected diagnostic categories
    st.session_state.form_data['diagnostic_category'] = st.multiselect(
        "Diagnostic Category (Check as many as apply):",
        options=[
            "Select Diagnostic Category",
            "Cardiac - Surgical",
            "Cardiac - Medical",
            "Respiratory - Upper Airway",
            "Respiratory - Lower Airway/Pulmonary",
            "Sepsis/Shock",
            "Neurological (excluding Traumatic Brain Injury)",
            "Trauma (including Traumatic Brain Injury)",
        ],
        default=st.session_state.form_data.get('diagnostic_category', [])
    )
    
    # Validation and navigation logic
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
            
            # Use .get() to safely check session_state keys
            if st.session_state.form_data.get('patient_gender', 'Select Gender') == "Select Gender":
                missing_fields.append("Patient Gender")
            if st.session_state.form_data.get('dosing_weight', "") == "":
                missing_fields.append("Patient Dosing Weight")
            if st.session_state.form_data.get('time', "") == "":
                missing_fields.append("Time")
            if st.session_state.form_data.get('location', "") == "":
                missing_fields.append("Location")
            if st.session_state.form_data.get('pager_number', "") == "":
                missing_fields.append("Pager Number")
            if st.session_state.form_data.get('family_member_present', 'Select if Family Member Present') == "Select if Family Member Present":
                missing_fields.append("Family Member Present")
            if st.session_state.form_data.get('attending_physician_present', 'Select if Attending Physician Present') == "Select if Attending Physician Present":
                missing_fields.append("Attending Physician Present")
            if st.session_state.form_data.get('airway_bundle', 'Select if Airway Bundle/Pink Sheet Completed') == "Select if Airway Bundle/Pink Sheet Present":
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
            st.session_state.page = "Summary"  # Set next page
            st.rerun()  # Rerun the app to reflect the new page



def send_email_with_attachment(to_emails, subject, body, pdf_buffer):
    # Email credentials from Streamlit secrets
    from_email = st.secrets["general"]["email"]
    password = st.secrets["general"]["email_password"]

    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_emails)  # Join multiple email addresses
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'html'))

    # Attach the PDF document
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf_buffer.read())  # Read PDF from the buffer
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="filled_form.pdf")
    msg.attach(part)

    # Send the email using SMTP with SSL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
            st.success("Email sent successfully with the PDF attachment!")
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
        
import io
import os
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
import streamlit as st

def set_need_appearances_writer(writer: PdfWriter):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer
    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

if st.session_state.page == "Summary":
    st.header("SUMMARY")

    # Optional: User email input
    user_email = st.text_input("Enter your email address (optional):", value="", key="user_email_input")

    if 'doc_file' not in st.session_state:
        st.session_state.doc_file = None

    # Create columns for navigation and submission buttons
    col_prev, col_submit = st.columns(2)

    with col_prev:
        if st.button("Previous"):
            st.session_state.page = "Disposition"
            st.rerun()

    with col_submit:
        if st.button("Submit"):
            # Collect form data into document_data dictionary
            document_data = {
                'airway_bundle': st.session_state.form_data['airway_bundle'],
                'date': st.session_state.form_data.get('date', ''),
                'time': st.session_state.form_data.get('time', ''),
                'location': st.session_state.form_data.get('location', ''),
                'patient_gender': st.session_state.form_data['patient_gender'],
                'weight': st.session_state.form_data['dosing_weight'],
                'form_completed_by': st.session_state.form_data['form_completed_by'],
                'pager_number': st.session_state.form_data['pager_number'],
                'family_member_present': st.session_state.form_data['family_member_present'],
                'attending_physician_present': st.session_state.form_data['attending_physician_present'],
                'indications': st.session_state['indications'],
                'type_of_change_from': st.session_state['type_of_change_from'],
                'type_of_change_to': st.session_state['type_of_change_to'],
                'nature_of_change': st.session_state['nature_of_change'],
                'tube_change_indications': st.session_state['tube_change_indications'],
                'diagnostic_category': ", ".join(st.session_state.form_data['diagnostic_category']) if isinstance(st.session_state.form_data.get('diagnostic_category', []), list) else st.session_state.form_data.get('diagnostic_category', ''),
                'difficult_to_bag': st.session_state['difficult_to_bag']
            }

            for attempt in range(1, 9):
                attempt_key = f"Attempt {attempt}"
                
                # Adding each attempt-related field to the document_data dictionary
                document_data[f'who_intubated_{attempt}'] = st.session_state.attempts[attempt_key]['who_intubated']
                document_data[f'discipline_{attempt}'] = st.session_state.attempts[attempt_key]['discipline']
                document_data[f'pgy_level_{attempt}'] = st.session_state.attempts[attempt_key]['pgy_level']
                document_data[f'ett_size_{attempt}'] = st.session_state.attempts[attempt_key]['ett_size']
                document_data[f'ett_type_{attempt}'] = st.session_state.attempts[attempt_key]['ett_type']
                document_data[f'cricoid_prior_{attempt}'] = st.session_state.attempts[attempt_key]['cricoid_prior']
                document_data[f'cricoid_during_{attempt}'] = st.session_state.attempts[attempt_key]['cricoid_during']
                document_data[f'attempt_successful_{attempt}'] = st.session_state.attempts[attempt_key]['attempt_successful']
            
            # Step 1: Convert the document_data dictionary to a pandas DataFrame
            df = pd.DataFrame([document_data])  # Wrap in a list to create a single-row DataFrame
            
            # Step 2: Convert the DataFrame to CSV
            csv_data = df.to_csv(index=False).encode('utf-8')

            # Step 3: Provide a download button for the CSV
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="form_data.csv",
                mime="text/csv"
            )

            # Step 4: Generate PDFs for the collected form data (in-memory)
            pdf_template = 'dcfx.pdf'  # Replace this with the correct path to your PDF template

            # Read the CSV from the in-memory bytes (csv_data)
            data = pd.read_csv(io.BytesIO(csv_data))

            data = data.fillna('') 

            # Read the PDF template
            pdf = PdfReader(pdf_template)  # Use PdfReader instead of PdfFileReader
            
            if "/AcroForm" in pdf.trailer["/Root"]:
                pdf.trailer["/Root"]["/AcroForm"].update(
                    {NameObject("/NeedAppearances"): BooleanObject(True)})

            # Create a PdfWriter instance for the new filled PDF
            pdf_writer = PdfWriter()

            # Loop through each row in the CSV data
            i = 0  # Filename numerical prefix
            for j, rows in data.iterrows():
                i += 1
                pdf_writer = PdfWriter()
                set_need_appearances_writer(pdf_writer)

                # Extract the form fields and map them to CSV row values
                field_dictionary_1 = {
                'airway_bundle': str(rows['airway_bundle']),
                'date': str(rows['date']),
                'time': str(rows['time']),
                'location': str(rows['location']),
                'patient_gender': str(rows['patient_gender']),
                'weight': str(rows['weight']),
                'formCompletedBy': str(rows['form_completed_by']),
                'pager_number': str(rows['pager_number']),
                'family_member_present': str(rows['family_member_present']),
                'attending_physician_present': str(rows['attending_physician_present']),
                'indications': str(rows['indications']),
                'type_of_change_from': str(rows['type_of_change_from']),
                'type_of_change_to': str(rows['type_of_change_to']),
                'nature_of_change': str(rows['nature_of_change']),
                'tube_change_indications': str(rows['tube_change_indications']),
                'diagnostic_category': str(rows['diagnostic_category']),
                'difficult_to_bag': str(rows['difficult_to_bag']),
                
                # Manually fill for each attempt
                'who_intubated_1': str(rows['who_intubated_1']),
                'discipline_1': str(rows['discipline_1']),
                'pgy_level_1': str(rows['pgy_level_1']),
                'ett_size_1': str(rows['ett_size_1']),
                'ett_type_1': str(rows['ett_type_1']),
                'cricoid_prior_1': str(rows['cricoid_prior_1']),
                'cricoid_during_1': str(rows['cricoid_during_1']),
                'attempt_successful_1': str(rows['attempt_successful_1']),
            
                'who_intubated_2': str(rows['who_intubated_2']),
                'discipline_2': str(rows['discipline_2']),
                'pgy_level_2': str(rows['pgy_level_2']),
                'ett_size_2': str(rows['ett_size_2']),
                'ett_type_2': str(rows['ett_type_2']),
                'cricoid_prior_2': str(rows['cricoid_prior_2']),
                'cricoid_during_2': str(rows['cricoid_during_2']),
                'attempt_successful_2': str(rows['attempt_successful_2']),
            
                'who_intubated_3': str(rows['who_intubated_3']),
                'discipline_3': str(rows['discipline_3']),
                'pgy_level_3': str(rows['pgy_level_3']),
                'ett_size_3': str(rows['ett_size_3']),
                'ett_type_3': str(rows['ett_type_3']),
                'cricoid_prior_3': str(rows['cricoid_prior_3']),
                'cricoid_during_3': str(rows['cricoid_during_3']),
                'attempt_successful_3': str(rows['attempt_successful_3']),
            
                'who_intubated_4': str(rows['who_intubated_4']),
                'discipline_4': str(rows['discipline_4']),
                'pgy_level_4': str(rows['pgy_level_4']),
                'ett_size_4': str(rows['ett_size_4']),
                'ett_type_4': str(rows['ett_type_4']),
                'cricoid_prior_4': str(rows['cricoid_prior_4']),
                'cricoid_during_4': str(rows['cricoid_during_4']),
                'attempt_successful_4': str(rows['attempt_successful_4']),
            
                'who_intubated_5': str(rows['who_intubated_5']),
                'discipline_5': str(rows['discipline_5']),
                'pgy_level_5': str(rows['pgy_level_5']),
                'ett_size_5': str(rows['ett_size_5']),
                'ett_type_5': str(rows['ett_type_5']),
                'cricoid_prior_5': str(rows['cricoid_prior_5']),
                'cricoid_during_5': str(rows['cricoid_during_5']),
                'attempt_successful_5': str(rows['attempt_successful_5']),
            
                'who_intubated_6': str(rows['who_intubated_6']),
                'discipline_6': str(rows['discipline_6']),
                'pgy_level_6': str(rows['pgy_level_6']),
                'ett_size_6': str(rows['ett_size_6']),
                'ett_type_6': str(rows['ett_type_6']),
                'cricoid_prior_6': str(rows['cricoid_prior_6']),
                'cricoid_during_6': str(rows['cricoid_during_6']),
                'attempt_successful_6': str(rows['attempt_successful_6']),
            
                'who_intubated_7': str(rows['who_intubated_7']),
                'discipline_7': str(rows['discipline_7']),
                'pgy_level_7': str(rows['pgy_level_7']),
                'ett_size_7': str(rows['ett_size_7']),
                'ett_type_7': str(rows['ett_type_7']),
                'cricoid_prior_7': str(rows['cricoid_prior_7']),
                'cricoid_during_7': str(rows['cricoid_during_7']),
                'attempt_successful_7': str(rows['attempt_successful_7']),
            
                'who_intubated_8': str(rows['who_intubated_8']),
                'discipline_8': str(rows['discipline_8']),
                'pgy_level_8': str(rows['pgy_level_8']),
                'ett_size_8': str(rows['ett_size_8']),
                'ett_type_8': str(rows['ett_type_8']),
                'cricoid_prior_8': str(rows['cricoid_prior_8']),
                'cricoid_during_8': str(rows['cricoid_during_8']),
                'attempt_successful_8': str(rows['attempt_successful_8'])
            }

                
                # Add the page to the writer and fill the form
                pdf_writer.add_page(pdf.pages[0])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[0], field_dictionary_1)
                pdf_writer.add_page(pdf.pages[1])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[1], field_dictionary_1)
                
                # Create a BytesIO stream to hold the output PDF
                pdf_output = io.BytesIO()
                pdf_writer.write(pdf_output)
                pdf_output.seek(0)  # Rewind to the beginning of the buffer

                unique_key = str(uuid.uuid4()) 
                
                # Provide the filled PDF for download
                st.download_button(
                    label=f"Download Filled PDF {i}",
                    data=pdf_output,
                    file_name=f"filled_form_{i}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_unique" 
                )
            subject = "White Form Submission"
            message = f"Here is the White Form.<br><br>Date: {document_data['date']}<br>Time: {document_data['time']}<br>Form Completed By: {document_data['form_completed_by']}"

            # Prepare recipients
            to_emails = [st.secrets["general"]["email_r"]]  # The designated email
            if user_email:  # Add user's email if provided
                to_emails.append(user_email)
        
            # Upload data to Firestore
            db = st.session_state.db
            db.collection("N4KFORMW").add(document_data)
            st.success("Form submitted successfully!")
        
            # Send email with the PDF attachment
            #send_email_with_attachment(to_emails, subject, message, pdf_output)

