import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import base64
from docx import Document
import io
import datetime

# Initialize Firebase
def initialize_firebase():
    if 'firebase_initialized' not in st.session_state:
        firebase_key = st.secrets["FIREBASE_KEY"]
        cred = credentials.Certificate(json.loads(firebase_key))
        
        try:
            firebase_admin.initialize_app(cred)
            st.session_state.firebase_initialized = True
        except ValueError as e:
            if "already exists" not in str(e):
                st.error(f"Failed to initialize Firebase: {str(e)}")

# Access Firestore
def get_firestore():
    if 'db' not in st.session_state:
        try:
            st.session_state.db = firestore.client()
        except Exception as e:
            st.error(f"Failed to connect to Firestore: {str(e)}")

# Form submission and document generation
def submit_form():
    if st.button("Submit"):
        try:
            db = st.session_state.db
            
            # Get values
            airway_bundle = st.session_state.form_data['airway_bundle']
            #selected_oxygen = st.session_state.selected_oxygen.strip()
            
            form_data = {
                "form_completed_by": st.session_state.form_data['form_completed_by'],
                "airway_bundle": airway_bundle,
                "date": st.session_state.form_data['date'].strftime("%Y-%m-%d"),  # Convert date to string
                "time": st.session_state.form_data['time'].strftime("%H:%M:%S"),  # Convert time to string
            }
            # Create a Word document
            doc = Document()
            doc.add_heading('Form Submission', level=1)
            for key, value in form_data.items():
                doc.add_paragraph(f"{key.replace('_', ' ').title()}: {value}")
            
            # Save the document to a BytesIO object
            doc_stream = io.BytesIO()
            doc.save(doc_stream)
            doc_stream.seek(0)

            # Encode the document in base64
            encoded_file = base64.b64encode(doc_stream.read()).decode('utf-8')

            # Upload form data
            form_ref = db.collection("N4KFORMW").add(form_data)
            st.success("Form submitted successfully!")

            # Upload document to Firestore
            file_data = {
                "file_name": "form_submission.docx",
                "file_content": encoded_file,
                "form_ref": form_ref.id
            }
            db.collection("UploadedDocuments").add(file_data)
            st.success("Document uploaded successfully!")

        except Exception as e:
            st.error(f"An error occurred while submitting the form: {e}")

# Streamlit app layout
def main():
    initialize_firebase()
    get_firestore()
    
    # Initialize form data
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            "form_completed_by": "",
            "airway_bundle": "",
            "date": "",
            "time": ""
        }

    st.header("Form Submission")

    st.session_state.form_data['form_completed_by'] = st.text_input("Completed By")
    st.session_state.form_data['airway_bundle'] = st.selectbox("Was the Airway Bundle Completed?", ["Yes", "No"])
    st.session_state.form_data['date'] = st.date_input("Date")
    st.session_state.form_data['time'] = st.time_input("Time")

    submit_form()

if __name__ == "__main__":
    main()
