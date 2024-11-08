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

    # Handle the multiselect for diagnostic categories
    if 'diagnostic_category' not in st.session_state.form_data:
        st.session_state.form_data['diagnostic_category'] = []

    st.session_state.diagnostic_category = st.multiselect(
        "Diagnostic Category (Check as many as apply):",
        options=[
            "Select Diagnostic Category",
            "Cardiac - Surgical",
            "Cardiac - Medical",
            "Respiratory - Upper Airway",
            "Respiratory - Lower Airway/Pulmonary",
            "Sepsis/Shock",
            "Neurological (excluding Traumatic Brain Injury)",
            "Trauma (including Traumatic Brain Injury",
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
            st.session_state.page = "Summary"  # Set next page
            st.rerun()  # Rerun the app to reflect the new page


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

from docx import Document

def create_word_doc(template_path, data):
    doc = Document(template_path)

    # Define your placeholders
    placeholders = {
        '{{date_placeholder}}': data['date'],
        '<<time_placeholder>>': data['time'],
        '<<location_placeholder>>': data['location'],
        '<<sex_placeholder>>': data['patient_gender'],
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
                'location': st.session_state.form_data.get('location',''),
                'patient_gender': st.session_state.form_data['patient_gender'],
                'weight': st.session_state.form_data['dosing_weight'],
                'form_completed_by':st.session_state.form_data['form_completed_by'],
                'pager_number':st.session_state.form_data['pager_number'],
                'family_member_present':st.session_state.form_data['family_member_present'],
                'attending_physician_present':st.session_state.form_data['attending_physician_present'],
                #'airway_bundle':st.session_state.form_data['airway_bundle'],
                'type_of_change_from':st.session_state['type_of_change_from'],
                #'type_of_change_to':st.session_state['type_of_change_to'],
                'diagnostic_category':st.session_state.form_data['diagnostic_category'],
            }
            st.write(st.session_state.form_data['date'])
            template_path = 'ntq.docx' 

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




