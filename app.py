import streamlit as st

# Title of the application
st.title("NEAR4KIDS QI COLLECTION FORM")

# Initialize session state if not already done
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Page 1
st.header("Patient Information")

# Page 2: Input Form
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
            options=list(range(1, 201)),  # Options from 1 to 200
            index=list(range(1, 201)).index(st.session_state.form_data.get('dosing_weight', 1))  # Default to 1 kg
        )

    # Third line: Diagnosis query
    st.write("AT THE TIME OF INTUBATION, did this patient have a suspected or confirmed diagnosis of an emerging epidemic/novel lung disease? (i.e. COVID-19, SARS, Pandemic Flu, EVALI)")
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
    
    # Submit button
    submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form submitted successfully!")
        # Here you can add code to handle the form data for your Word document
        st.write(st.session_state.form_data)  # For debugging: display the form data
