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
import ast 

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
            width: 100%;                  /* Ensure it fills the column */
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
            "Email Address:", 
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
    st.session_state.form_data['supervisor'] = st.selectbox(
            "Attending Supervisor:", 
            options=["No Supervisor", "ckrawiec@pennstatehealth.psu.edu", "", ""], 
            index=["No Supervisor", "ckrawiec@pennstatehealth.psu.edu", "", ""].index(st.session_state.form_data.get('supervisor', 'No Supervisor'))
        )
        
    if 'diagnostic_category' not in st.session_state.form_data:
        st.session_state.form_data['diagnostic_category'] = []
    
    # Ensure the session state is updated after the interaction (before widget renders)
    
    other_category = None
    
    diagnostic_category = st.multiselect(
        "Diagnostic Category (Check as many as apply):",
        options=[
            "Cardiac - Surgical",
            "Cardiac - Medical",
            "Respiratory - Upper Airway",
            "Respiratory - Lower Airway/Pulmonary",
            "Sepsis/Shock",
            "Neurological (excluding Traumatic Brain Injury)",
            "Trauma (including Traumatic Brain Injury)",
            "Other"  # Adding the "Other" option
        ],
        default=st.session_state.form_data.get('diagnostic_category', [])  # Default from session state
    )
    
    # If "Other" is selected, show a text input for custom category
    if "Other" in diagnostic_category:
        other_category = st.text_input("Please specify the 'Other' category:")
    
    # Only update session state if "Other" is specified
    if other_category:
        # Add the custom 'Other' category to the list
        diagnostic_category.append(other_category)
    # Validation and navigation logic
    col_prev, col_next = st.columns(2)
    #with col_prev:
    #    if st.button("Previous"):
    #        st.session_state.page = "Starting Page"
    #        st.rerun()
    
    with col_next:
        # Only proceed if button is clicked
        if st.button("Next"):
            if diagnostic_category != st.session_state.form_data['diagnostic_category']:
                st.session_state.form_data['diagnostic_category'] = diagnostic_category
            st.session_state.page = "Indications"  # Set next page
            st.rerun()
                
            # Validation check for required fields
            #missing_fields = []
            
            # Use .get() to safely check session_state keys
            #if st.session_state.form_data.get('patient_gender', 'Select Gender') == "Select Gender":
            #    missing_fields.append("Patient Gender")
            #if st.session_state.form_data.get('dosing_weight', "") == "":
            #    missing_fields.append("Patient Dosing Weight")
            #if st.session_state.form_data.get('time', "") == "":
            #    missing_fields.append("Time")
            #if st.session_state.form_data.get('location', "") == "":
            #    missing_fields.append("Location")
            #if st.session_state.form_data.get('pager_number', "") == "":
            #    missing_fields.append("Pager Number")
            #if st.session_state.form_data.get('family_member_present', 'Select if Family Member Present') == "Select if Family Member Present":
            #    missing_fields.append("Family Member Present")
            #if st.session_state.form_data.get('attending_physician_present', 'Select if Attending Physician Present') == "Select if Attending Physician Present":
            #    missing_fields.append("Attending Physician Present")
            #if st.session_state.form_data.get('airway_bundle', 'Select if Airway Bundle/Pink Sheet Completed') == "Select if Airway Bundle/Pink Sheet Present":
            #    missing_fields.append("Airway Bundle/Pink Sheet Present")
    
            #if missing_fields:
            #    st.warning(f"Please fill in the following: {', '.join(missing_fields)}")
            #else:
            #    st.session_state.page = "Indications"  # Set next page
            #    st.rerun()


elif st.session_state.page == "Indications":
    # Indications section
    st.markdown("<h2 style='text-align: center;'>INDICATIONS</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center;'>INITIAL INTUBATION</h3>", unsafe_allow_html=True)
        indications = st.multiselect(
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
            st.session_state.type_of_change_from = st.selectbox("Type of Change From:", options=["","Oral", "Nasal", "Tracheostomy"], index=["","Oral", "Nasal", "Tracheostomy"].index(st.session_state.get('type_of_change_from', '')))
        with col4:
            st.session_state.type_of_change_to = st.selectbox("Type of Change To:", options=["","Oral", "Nasal", "Tracheostomy"], index=["","Oral", "Nasal", "Tracheostomy"].index(st.session_state.get('type_of_change_to', '')))

        st.session_state.nature_of_change = st.selectbox("Nature of Change:", 
            options=["","Clinical Condition", "Immediate Post-Intubation (Exclude Tracheostomy Change)"],
            index=["","Clinical Condition", "Immediate Post-Intubation (Exclude Tracheostomy Change)"].index(st.session_state.get('nature_of_change', ''))
        )

        tube_change_indications = st.multiselect(
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
            st.session_state['indications'] = indications
            st.session_state['tube_change_indications'] = tube_change_indications
            st.session_state.page = "Encounter Information"  # Navigate back to the previous page
            st.rerun()  # Rerun the app to reflect the new page

    with col_next:
        if st.button("Next"):
            st.session_state['indications'] = indications
            st.session_state['tube_change_indications'] = tube_change_indications
            
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
        # Ensure session state is initialized for each question
    if "evaluation_1" not in st.session_state:
        st.session_state["evaluation_1"] = 'Select Category 1'
    if "evaluation_2" not in st.session_state:
        st.session_state["evaluation_2"] = 'Select Category 2'
    if "evaluation_3" not in st.session_state:
        st.session_state["evaluation_3"] = 'Select Category 3'
    if "evaluation_4" not in st.session_state:
        st.session_state["evaluation_4"] = 'Select Category 4'
    if "evaluation_5" not in st.session_state:
        st.session_state["evaluation_5"] = 'Select Category 5'
    if "evaluation_6" not in st.session_state:
        st.session_state["evaluation_6"] = 'Select Category 6'
    if "evaluation_7" not in st.session_state:
        st.session_state["evaluation_7"] = 'Select Category 7'
    if "evaluation_8" not in st.session_state:
        st.session_state["evaluation_8"] = 'Select Category 8'
    if "evaluation_9" not in st.session_state:
        st.session_state["evaluation_9"] = ''
        
    # Define the questions and options
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
    for i in range(1, 9):
        if f"evaluation_{i}" not in st.session_state:
            st.session_state[f"evaluation_{i}"] = f'Select Category {i}'

    # Create the layout for questions and options
    for i, (question, options) in enumerate(questions, 1):
        cols = st.columns([4, 1])  # Adjust columns if needed
        
        with cols[0]:  # Question column
            question_box(f"{i}. {question}")
        
        with cols[1]:  # Dropdown column
            selected_option = st.selectbox(
                "",
                options=options,
                index=options.index(st.session_state[f"evaluation_{i}"]),
                key=f"evaluation_{i}_selectbox",
                help=f"Select an option for {question}"  # Optional help text
            )
            st.session_state[f"evaluation_{i}"] = selected_option

    # If the last question is answered with "YES", ask for more details
    if st.session_state["evaluation_8"] == 'YES':
        cols = st.columns([4, 1])
        with cols[0]:
            st.write("Please provide details:")
        with cols[1]:
            user_input = st.text_input(
                "Enter any other signs of difficult airway",
                key="evaluation_9_input"  # New session state key for this input
            )
            st.session_state["evaluation_9"] = user_input


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
        "other_1":"",
        "rocuronium_dose": "",
        "succinylcholine_dose": "",
        "pancuronium_dose": "",
        "cisatracuronium_dose": "",
        "other_2":"",
        "propofol_dose": "",
        "etomidate_dose": "",
        "ketamine_dose": "",
        "midazolam_dose": "",
        "thiopental_dose": "",
        "other_3":"",
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
            other_1 = st.text_input("mg Other", value=st.session_state.other_1, key="other_1_input")

        with col2:
            st.markdown("### Paralysis Dosage")
            rocuronium_input = st.text_input("mg Rocuronium", value=st.session_state.rocuronium_dose, key="rocuronium_dose_input")
            succinylcholine_input = st.text_input("mg Succinylcholine", value=st.session_state.succinylcholine_dose, key="succinylcholine_dose_input")
            vecuronium_paralysis_input = st.text_input("mg Vecuronium", value=st.session_state.vecuronium_paralysis_dose, key="vecuronium_paralysis_dose_input")
            pancuronium_input = st.text_input("mg Pancuronium", value=st.session_state.pancuronium_dose, key="pancuronium_dose_input")
            cisatracuronium_input = st.text_input("mg Cisatracuronium", value=st.session_state.cisatracuronium_dose, key="cisatracuronium_dose_input")
            other_2 = st.text_input("mg Other", value=st.session_state.other_2, key="other_2_input")

        with col3:
            st.markdown("### Induction Dosage")
            propofol_input = st.text_input("mg Propofol", value=st.session_state.propofol_dose, key="propofol_dose_input")
            etomidate_input = st.text_input("mg Etomidate", value=st.session_state.etomidate_dose, key="etomidate_dose_input")
            ketamine_input = st.text_input("mg Ketamine", value=st.session_state.ketamine_dose, key="ketamine_dose_input")
            midazolam_input = st.text_input("mg Midazolam", value=st.session_state.midazolam_dose, key="midazolam_dose_input")
            thiopental_input = st.text_input("mg Thiopental", value=st.session_state.thiopental_dose, key="thiopental_dose_input")
            other_3 = st.text_input("mg Other", value=st.session_state.other_3, key="other_3_input")

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
        st.session_state.other_1 = ""
        st.session_state.rocuronium_dose = ""
        st.session_state.succinylcholine_dose = ""
        st.session_state.pancuronium_dose = ""
        st.session_state.cisatracuronium_dose = ""
        st.session_state.other_2 = ""
        st.session_state.propofol_dose = ""
        st.session_state.etomidate_dose = ""
        st.session_state.ketamine_dose = ""
        st.session_state.midazolam_dose = ""
        st.session_state.thiopental_dose = ""
        st.session_state.other_3 = ""
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
                st.session_state.other_1 = other_1
                st.session_state.rocuronium_dose = rocuronium_input
                st.session_state.succinylcholine_dose = succinylcholine_input
                st.session_state.vecuronium_paralysis_dose = vecuronium_paralysis_input
                st.session_state.pancuronium_dose = pancuronium_input
                st.session_state.cisatracuronium_dose = cisatracuronium_input
                st.session_state.other_2 = other_2
                st.session_state.propofol_dose = propofol_input
                st.session_state.etomidate_dose = etomidate_input
                st.session_state.ketamine_dose = ketamine_input
                st.session_state.midazolam_dose = midazolam_input
                st.session_state.thiopental_dose = thiopental_input
                st.session_state.other_3 = other_3
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
            st.session_state.selected_techniques = selected_techniques
            st.session_state.page = "Method Details"  # Set next page (update this to your actual next page)
            st.rerun()

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
            st.session_state.selected_methods = selected_methods 
            st.session_state.page = "Method"  # Update this to your actual previous page
            st.rerun()  # Refresh the app to apply changes

    with col2:
        if st.button("Next"):
            st.session_state.selected_methods = selected_methods  # Save selected methods to session state
            
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
    

    if "other_event_description" not in st.session_state:
            st.session_state.other_event_description = ""
            
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
            st.session_state.selected_confirmation = selected_confirmation
            st.session_state.selected_events = selected_events
            st.session_state.page = "Method Details"
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.selected_confirmation = selected_confirmation  # Save selection
            st.session_state.selected_events = selected_events  # Save selection
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
    
        # Check if input can be converted to an integer
        if highest_value != "":
            try:
                st.session_state.highest_value = int(highest_value)
            except ValueError:
                st.session_state.highest_value = ""  # Reset if invalid
                st.error("Please enter a valid integer for Highest Value.")
    
    # Lowest Value Input
    if "lowest_value" not in st.session_state:
        st.session_state.lowest_value = ""  # Initialize if not present
    
    with cols[1]:
        lowest_value = st.text_input("Lowest value during intubation:", value=st.session_state.lowest_value)
    
        # Check if input can be converted to an integer
        if lowest_value != "":
            try:
                st.session_state.lowest_value = int(lowest_value)
            except ValueError:
                st.session_state.lowest_value = ""  # Reset if invalid
                st.error("Please enter a valid integer for Lowest Value.")

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

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
from io import BytesIO
import streamlit as st

def send_email_with_attachment2(to_emails, subject, body, pdf_url):
    # Email credentials from Streamlit secrets
    from_email = st.secrets["general"]["email"]
    password = st.secrets["general"]["email_password"]

    # Download the PDF from the GitHub URL
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Check if the request was successful
        pdf_buffer = BytesIO(response.content)  # Convert the content to a file-like object
    except requests.exceptions.RequestException as e:
        st.error(f"Error downloading PDF: {e}")
        return

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
    part.add_header('Content-Disposition', 'attachment', filename="test.pdf")
    msg.attach(part)

    # Send the email using SMTP with SSL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
            st.success("Email sent successfully with the PDF attachment!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import streamlit as st

def send_email_without_attachment(to_emails, subject, body):
    """
    Sends an email without any attachment.

    Args:
    - to_emails (list): List of recipient email addresses.
    - subject (str): Subject of the email.
    - body (str): HTML body content of the email.
    """
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
            # Convert `attempt_mapping` to a Firestore-friendly format
            attempt_mapping_data = {str(attempt): events for attempt, events in st.session_state['attempt_mapping'].items()}

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
                'difficult_to_bag': st.session_state['difficult_to_bag'],
                'evaluation_1': st.session_state['evaluation_1'],
                'evaluation_2': st.session_state['evaluation_2'],
                'evaluation_3': st.session_state['evaluation_3'],
                'evaluation_4': st.session_state['evaluation_4'],
                'evaluation_5': st.session_state['evaluation_5'],
                'evaluation_6': st.session_state['evaluation_6'],
                'evaluation_7': st.session_state['evaluation_7'],
                'evaluation_8': st.session_state['evaluation_8'],
                'evaluation_9': st.session_state['evaluation_9'],
                'cyanotic': st.session_state['cyanotic'],
                
                'no_drugs':st.session_state['no_drugs'],
                'atropine_dose':st.session_state['atropine_dose'],
                'glycopyrrolate_dose':st.session_state['glycopyrrolate_dose'],
                'fentanyl_dose':st.session_state['fentanyl_dose'],
                'lidocaine_dose':st.session_state['lidocaine_dose'],
                'vecuronium_dose':st.session_state['vecuronium_dose'],
                'other_1':st.session_state['other_1'],

                'rocuronium_dose':st.session_state['rocuronium_dose'],
                'succinylcholine_dose':st.session_state['succinylcholine_dose'],
                'vecuronium_paralysis_dose':st.session_state['vecuronium_paralysis_dose'],
                'pancuronium_dose':st.session_state['pancuronium_dose'],
                'cisatracuronium_dose':st.session_state['cisatracuronium_dose'],
                'other_2':st.session_state['other_2'],

                'propofol_dose':st.session_state['propofol_dose'],
                'etomidate_dose':st.session_state['etomidate_dose'],
                'ketamine_dose':st.session_state['ketamine_dose'],
                'midazolam_dose':st.session_state['midazolam_dose'],
                'thiopental_dose':st.session_state['thiopental_dose'],
                'other_3':st.session_state['other_3'],

                'atropine_indications':st.session_state['atropine_indications'],
                'glycopyrrolate_indications':st.session_state['glycopyrrolate_indications'],
                
                'selected_method':st.session_state['selected_method'],
                'selected_techniques':st.session_state['selected_techniques'],
                
                'selected_oxygen':st.session_state['selected_oxygen'],
                'selected_methods':st.session_state['selected_methods'],

                'liter_flow':st.session_state['liter_flow'],
                'fio2':st.session_state['fio2'],

                'selected_events':st.session_state['selected_events'],
                #'attempt_mapping':st.session_state['attempt_mapping'],

                'other_event_description':st.session_state['other_event_description'],

                'selected_device':st.session_state['selected_device'],
                'selected_confirmation':st.session_state['selected_confirmation'],
                'glottic_exposure':st.session_state['glottic_exposure'],

                'highest_value':st.session_state['highest_value'],
                'lowest_value':st.session_state['lowest_value'],
                'course_success':st.session_state['course_success'],

                'disposition':st.session_state['disposition'],
                'other_disposition':st.session_state['other_disposition'],
                
                'other_comments':st.session_state['other_comments'],

                "attempt_mapping": attempt_mapping_data, 

                "transferred_to_PICU": st.session_state['transferred_to_PICU'],
                "transferred_to_NICU": st.session_state['transferred_to_NICU'],
                "transferred_to_CICU": st.session_state['transferred_to_CICU'],

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

            # Step 3: Generate PDFs for the collected form data (in-memory)
            pdf_template = 'dcfx.pdf'  # Replace this with the correct path to your PDF template

            # Read the CSV from the in-memory bytes (csv_data)
            data = pd.read_csv(io.BytesIO(csv_data))

            for i in range(1, 8):  # Loop to add columns for 1 to 7
                data[f"selected_methods{i}"] = ""
                data[f"liter_flow_{i}"] = ""
                data[f"fio2_{i}"] = ""

            for i in range(1, 22):  # Loop to add columns for 1 to 21
                data[f"attempt_{i}"] = ""

            for i in range(1, 6):  # Loop to add columns for 1 to 7
                data[f"disposition_{i}"] = ""

            # Assuming the 'selected_methods' column contains string representations of lists
            
            data['selected_methods'] = data['selected_methods'].apply(ast.literal_eval)
            
            # Predefined list of methods for reference (the order will be used for column names)
            predefined_methods = [
                'NC without nasal airway', 
                'NC with nasal airway', 
                'Oral airway with oxygen port', 
                'Through LMA', 
                'HFNC', 
                'NIV with nasal prong interface – provide PEEP/PIP', 
                'Other (device, FiO2, Setting)'
            ]
            
            # Assuming 'liter_flow' and 'fio2' columns contain a dictionary with flow and FiO2 values
            data['liter_flow'] = data['liter_flow'].apply(ast.literal_eval)
            data['fio2'] = data['fio2'].apply(ast.literal_eval)
            
            # Now process the 'selected_methods' column to assign methods to specific columns
            for i, method in enumerate(predefined_methods):
                # Create column names like selected_methods1, selected_methods2, etc.
                selected_column_name = f'selected_methods{i + 1}'
                liter_flow_column_name = f'liter_flow_{i + 1}'
                fio2_column_name = f'fio2_{i + 1}'
            
                # Initialize all the columns with an empty string
                data[selected_column_name] = ""
                data[liter_flow_column_name] = ""
                data[fio2_column_name] = ""
            
                # Check if the method is selected (it will be in the 'selected_methods' list)
                if method in data['selected_methods'][0]:
                    # If method is selected, place "X" in the corresponding selected_methods column
                    data[selected_column_name] = "X"
            
                    # Assign the corresponding liter flow value to the liter_flow column
                    liter_flow_key = f'liter_flow_{method.replace(" ", "_")}'
                    fio2_key = f'fio2_{method.replace(" ", "_")}'
            
                    # Assign the liter flow value if it exists in the dictionary, else leave it empty
                    if liter_flow_key in data['liter_flow'][0]:
                        data[liter_flow_column_name] = data['liter_flow'][0].get(liter_flow_key, "")
                    
                    # Assign the fio2 value if it exists in the dictionary, else leave it empty
                    if fio2_key in data['fio2'][0]:
                        data[fio2_column_name] = data['fio2'][0].get(fio2_key, "")
            
            data['selected_events'] = data['selected_events'].apply(ast.literal_eval)
            
            # Predefined list of methods for reference (the order will be used for column names)
            predefined_methods = [
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

            for i, method in enumerate(predefined_methods):
                # Create column names like selected_methods1, selected_methods2, etc.
                selected_column_name = f'event_{i + 1}'
            
                # Initialize all the columns with an empty string
                data[selected_column_name] = ""
            
                if method in data['selected_events'][0]:
                    data[selected_column_name] = "X"

            for attempt_num in range(1, 22):
                data[f'attempt_{attempt_num}'] = ''
            
            # Step 5: Deserialize the 'attempt_mapping' and map the events to attempt columns
            if 'attempt_mapping' in data.columns:
                attempt_mapping_str = data['attempt_mapping'][0]
            
                # Preprocess the string to convert single quotes to double quotes (for valid JSON format)
                attempt_mapping_str = attempt_mapping_str.replace("'", '"')
            
                try:
                    # Deserialize the attempt_mapping
                    attempt_mapping = json.loads(attempt_mapping_str)
                except Exception as e:
                    print(f"Error deserializing 'attempt_mapping': {e}")
            else:
                raise ValueError("The 'attempt_mapping' column is missing from the CSV.")
            
            # Step 6: Map attempts to the corresponding event columns in the same row
            for attempt_num, events in attempt_mapping.items():
                attempt_num = int(attempt_num)  # Ensure attempt_num is an integer
            
                # For each event in the list for this attempt
                for event in events:
                    if event in predefined_methods:
                        event_index = predefined_methods.index(event) + 1  # event_1, event_2, etc. (1-based index)
                        event_column = f'event_{event_index}'
            
                        # If the event is marked with "X" in the respective event column, process the attempts
                        if data.at[0, event_column] == "X":
                            # Get the current attempt data for this event column (for tracking attempts)
                            current_attempts = data.at[0, f'attempt_{event_index}']
            
                            # If there are existing attempts, append the current attempt number
                            if current_attempts:
                                current_attempts = f"{current_attempts}, {attempt_num}"
                            else:
                                current_attempts = str(attempt_num)
            
                            # Update the attempt column with the new attempt number
                            data.at[0, f'attempt_{event_index}'] = current_attempts
                        else:
                            print(f"Event '{event}' not marked with 'X' in the event column.")
                    else:
                        print(f"Event '{event}' not found in predefined_methods list.")
            
            predefined_methods = ["Stay in PICU/NICU/CICU/ED",
            "Transferred to",
            "Died – due to failed airway management",
            "Died – other causes",
            "Other"]
            
            for i, method in enumerate(predefined_methods):
                # Create column names like selected_methods1, selected_methods2, etc.
                selected_column_name = f'disposition_{i + 1}'

                if method in data['disposition'][0]:
                        # If method is selected, place "X" in the corresponding selected_methods column
                        data[selected_column_name] = "X"
                
            data['no_drugs'] = data['no_drugs'].replace("NO DRUGS USED", "X")
            data['no_drugs'] = data['no_drugs'].replace("DRUGS USED", "")
            
            data['transferred_to_PICU'] = data['transferred_to_PICU'].apply(
                lambda x: 'X' if x == True else '' if x == False else x
            )
            
            data['transferred_to_NICU'] = data['transferred_to_NICU'].apply(
                lambda x: 'X' if x == True else '' if x == False else x
            )
            
            data['transferred_to_CICU'] = data['transferred_to_CICU'].apply(
                lambda x: 'X' if x == True else '' if x == False else x
            )

            data['tube_change_indications'] = data['tube_change_indications'].apply(ast.literal_eval)
            data['tube_change_indications'] = data['tube_change_indications'].apply(lambda x: ', '.join(f"'{item}'" for item in x))
            
            data['indications'] = data['indications'].apply(ast.literal_eval)
            data['indications'] = data['indications'].apply(lambda x: ', '.join(f"'{item}'" for item in x))
            
            data['atropine_indications'] = data['atropine_indications'].apply(ast.literal_eval)
            data['atropine_indications'] = data['atropine_indications'].apply(lambda x: ', '.join(f"'{item}'" for item in x))
            
            data['glycopyrrolate_indications'] = data['glycopyrrolate_indications'].apply(ast.literal_eval)
            data['glycopyrrolate_indications'] = data['glycopyrrolate_indications'].apply(lambda x: ', '.join(f"'{item}'" for item in x))
            
            data['selected_techniques'] = data['selected_techniques'].apply(ast.literal_eval)
            data['selected_techniques'] = data['selected_techniques'].apply(lambda x: ', '.join(f"'{item}'" for item in x))
            
            data['selected_confirmation'] = data['selected_confirmation'].apply(ast.literal_eval)
            data['selected_confirmation'] = data['selected_confirmation'].apply(lambda x: ', '.join(f"'{item}'" for item in x))

            data = data.fillna('')
            
            csv_data = data.to_csv(index=False).encode('utf-8')
            
            # Step 3: Provide a download button for the CSV
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="form_data.csv",
                mime="text/csv"
            )
            
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
                'attempt_successful_8': str(rows['attempt_successful_8']),

                'evaluation_1': str(rows['evaluation_1']),
                'evaluation_2': str(rows['evaluation_2']),
                'evaluation_3': str(rows['evaluation_3']),
                'evaluation_4': str(rows['evaluation_4']),
                'evaluation_5': str(rows['evaluation_5']),
                'evaluation_6': str(rows['evaluation_6']),
                'evaluation_7': str(rows['evaluation_7']),
                'evaluation_8': str(rows['evaluation_8']),    
                'evaluation_9': str(rows['evaluation_9']),

                'cyanotic': str(rows['cyanotic']),

                'no_drugs': str(rows['no_drugs']),
                'atropine_dose': str(rows['atropine_dose']),
                'glycopyrrolate_dose': str(rows['glycopyrrolate_dose']),
                'fentanyl_dose': str(rows['fentanyl_dose']),
                'lidocaine_dose': str(rows['lidocaine_dose']),
                'vecuronium_dose': str(rows['vecuronium_dose']),
                'other_1':str(rows['other_1']),
                'rocuronium_dose': str(rows['rocuronium_dose']),
                'succinylcholine_dose': str(rows['succinylcholine_dose']),
                'vecuronium_paralysis_dose': str(rows['vecuronium_paralysis_dose']),
                'pancuronium_dose': str(rows['pancuronium_dose']),
                'cisatracuronium_dose': str(rows['cisatracuronium_dose']),
                'other_2':str(rows['other_2']),
                'propofol_dose': str(rows['propofol_dose']),
                'etomidate_dose': str(rows['etomidate_dose']),
                'ketamine_dose': str(rows['ketamine_dose']),
                'midazolam_dose': str(rows['midazolam_dose']),
                'thiopental_dose': str(rows['thiopental_dose']),
                'other_3':str(rows['other_3']),
                
                'selected_method': str(rows['selected_method']),
                'selected_techniques': str(rows['selected_techniques']),
                
                'selected_oxygen': str(rows['selected_oxygen']),
                'selected_methods': str(rows['selected_methods']),

                'selected_confirmation': str(rows['selected_confirmation']),

                'glottic_exposure': str(rows['glottic_exposure']),

                'highest_value': str(rows['highest_value']),
                'lowest_value': str(rows['lowest_value']),

                'course_success': str(rows['course_success']),

                'selected_methods1': str(rows['selected_methods1']),
                'selected_methods2': str(rows['selected_methods2']),
                'selected_methods3': str(rows['selected_methods3']),
                'selected_methods4': str(rows['selected_methods4']),
                'selected_methods5': str(rows['selected_methods5']),
                'selected_methods6': str(rows['selected_methods6']),
                'selected_methods7': str(rows['selected_methods7']),
            
                'liter_flow': str(rows['liter_flow']),
                'liter_flow_1': str(rows['liter_flow_1']),
                'liter_flow_2': str(rows['liter_flow_2']),
                'liter_flow_3': str(rows['liter_flow_3']),
                'liter_flow_4': str(rows['liter_flow_4']),
                'liter_flow_5': str(rows['liter_flow_5']),
                #'liter_flow_6': str(rows['liter_flow_6']),
                'liter_flow_7': str(rows['liter_flow_7']),
            
                'fio2': str(rows['fio2']),
                'fio2_1': str(rows['fio2_1']),
                'fio2_2': str(rows['fio2_2']),
                'fio2_3': str(rows['fio2_3']),
                'fio2_4': str(rows['fio2_4']),
                'fio2_5': str(rows['fio2_5']),
                'fio2_6': str(rows['fio2_6']),
                'fio2_7': str(rows['fio2_7']),
                                                           
                'selected_device': str(rows['selected_device']),
                'atropine_indications':str(rows['atropine_indications']),
                'glycopyrrolate_indications':str(rows['glycopyrrolate_indications']),

                'event_1': str(rows['event_1']),
                'event_2': str(rows['event_2']),
                'event_3': str(rows['event_3']),
                'event_4': str(rows['event_4']),
                'event_5': str(rows['event_5']),
                'event_6': str(rows['event_6']),
                'event_7': str(rows['event_7']),
                'event_8': str(rows['event_8']),
                'event_9': str(rows['event_9']),
                'event_10': str(rows['event_10']),
                'event_11': str(rows['event_11']),
                'event_12': str(rows['event_12']),
                'event_13': str(rows['event_13']),
                'event_14': str(rows['event_14']),
                'event_15': str(rows['event_15']),
                'event_16': str(rows['event_16']),
                'event_17': str(rows['event_17']),
                'event_18': str(rows['event_18']),
                'event_19': str(rows['event_19']),
                'event_20': str(rows['event_20']),
                'event_21': str(rows['event_21']),

                'attempt_1': str(rows['attempt_1']),
                'attempt_2': str(rows['attempt_2']),
                'attempt_3': str(rows['attempt_3']),
                'attempt_4': str(rows['attempt_4']),
                'attempt_5': str(rows['attempt_5']),
                'attempt_6': str(rows['attempt_6']),
                'attempt_7': str(rows['attempt_7']),
                'attempt_8': str(rows['attempt_8']),
                'attempt_9': str(rows['attempt_9']),
                'attempt_10': str(rows['attempt_10']),
                'attempt_11': str(rows['attempt_11']),
                'attempt_12': str(rows['attempt_12']),
                'attempt_13': str(rows['attempt_13']),
                'attempt_14': str(rows['attempt_14']),
                'attempt_15': str(rows['attempt_15']),
                'attempt_16': str(rows['attempt_16']),
                'attempt_17': str(rows['attempt_17']),
                'attempt_18': str(rows['attempt_18']),
                'attempt_19': str(rows['attempt_19']),
                'attempt_20': str(rows['attempt_20']),
                'attempt_21': str(rows['attempt_21']),
                
                'other_comments': str(rows['other_comments']),


                'other_event_description': str(rows['other_event_description']),

                "picu": str(rows['transferred_to_PICU']),
                "nicu": str(rows['transferred_to_NICU']),
                "cicu": str(rows['transferred_to_CICU']),

                'disposition_1': str(rows['disposition_1']),
                'disposition_2': str(rows['disposition_2']),
                'disposition_3': str(rows['disposition_3']),
                'disposition_4': str(rows['disposition_4']),
                'disposition_5': str(rows['disposition_5']),

            }

                
                # Add the page to the writer and fill the form
                pdf_writer.add_page(pdf.pages[0])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[0], field_dictionary_1)
                
                pdf_writer.add_page(pdf.pages[1])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[1], field_dictionary_1)
                
                pdf_writer.add_page(pdf.pages[2])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[2], field_dictionary_1)

                pdf_writer.add_page(pdf.pages[3])
                pdf_writer.update_page_form_field_values(pdf_writer.pages[3], field_dictionary_1)
                
                # Create a BytesIO stream to hold the output PDF
                pdf_output = io.BytesIO()
                pdf_writer.write(pdf_output)
                pdf_output.seek(0)  # Rewind to the beginning of the buffer


                st.download_button(
                    label=f"Download Filled PDF {i}",
                    data=pdf_output,
                    file_name=f"filled_form_{i}.pdf",
                    mime="application/pdf",
                    key=f"download_pdf_unique" 
                )

           ####WHITE FORM SUBMISSION#####
            subject = "White Form Submission"
            message = f"Here is the White Form.<br><br>Date: {document_data['date']}<br>Time: {document_data['time']}<br>Form Completed By: {document_data['form_completed_by']}"
    
            to_emails = [st.secrets["general"]["email_r"]]  # The designated email
            
            if user_email:  # Add user's email if provided
                to_emails.append(user_email)

            # Upload data to Firestore
            db = st.session_state.db
            db.collection("N4KFORMW").add(document_data)
            st.success("Form submitted successfully!")
        
            # Send email with the PDF attachment
            #send_email_with_attachment(to_emails, subject, message, pdf_output)

            # Safely retrieve the 'lowest_value' from session state and ensure it's a number
            lowest_value = st.session_state.get('lowest_value', None)
            
            # Only proceed if the 'lowest_value' is a valid integer
            if lowest_value is not None:
                try:
                    # Convert 'lowest_value' to an integer
                    lowest_value_int = int(lowest_value)
                
                    # Now compare it numerically
                    if lowest_value_int <= 80:
                        # Initialize the email list with the designated email
                        to_emails1 = [st.secrets["general"]["email_r"]]  # The designated email
                    
                        # Check if there's a supervisor email and add it to the list if it's valid
                        supervisor_email = st.session_state.form_data.get('supervisor', 'No Supervisor')
                        if supervisor_email and supervisor_email != "No Supervisor":
                            to_emails1.append(supervisor_email)
                    
                        # Define the email subject and message
                        subject1 = "N4KIDS FEEDBACK ALERT"
                        message1 = f"""
                        Hi, 
                        It has come to our attention that your trainee experienced a Tracheal Intubation Adverse Event. The lowest saturation value reported was: {document_data['lowest_value']}
                        Use this link to provide feedback to your trainee: https://hmcn4kfbform.streamlit.app/ <br><br>
                        Date: {document_data['date']}<br>
                        Time: {document_data['time']}<br>
                        Form Completed By: {document_data['form_completed_by']}
                        """
                    
                        # Call the function to send the email **without the PDF attachment**
                        send_email_without_attachment(to_emails1, subject1, message1)
                    
                except ValueError:
                    # If the 'lowest_value' cannot be converted to an integer, handle it
                    st.error("The 'lowest_value' entered is not a valid number. Please provide a valid integer.")
            else:
                st.error("The 'lowest_value' is missing. Please provide the lowest value for the saturation.")

            if st.session_state.get('airway_bundle') == 'No':
                # Initialize the email list with the designated email
                to_emails1 = [st.secrets["general"]["email_r"]]  # The designated email
            
                # Check if there's a supervisor email and add it to the list if it's valid
                if pager_number:  # Add user's email if provided
                    to_emails1.append(pager_number)
            
                # Define the email subject and message
                subject1 = "N4KIDS AIRWAY BUNDLE ALERT"
                message1 = f"""
                Hi, 
                It has come to our attention that the airway bundle was not utilized for this airway course. If you did utilize a checklist, please utilize this attachment and complete the form. Thank you! 
                Use the attached tool to provide feedback to your trainee. <br><br>
                Date: {document_data['date']}<br>
                Time: {document_data['time']}<br>
                Form Completed By: {document_data['form_completed_by']}
                """
            
                # Define the URL for the PDF attachment (hosted on GitHub)
                pdf_url = 'https://raw.githubusercontent.com/conkraw/n4kform/main/test.pdf'
            
                # Call the function to send the email with the PDF attachment
                send_email_with_attachment2(to_emails1, subject1, message1, pdf_url)
