import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from docx import Document
import io
import base64

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

# Submit form and upload document
def submit_form(text_input):
    if st.button("Submit"):
        try:
            db = st.session_state.db
            
            # Create a Word document
            doc = Document()
            doc.add_heading('Text Input Submission', level=1)
            doc.add_paragraph(text_input)
            
            # Save the document to a BytesIO object
            doc_stream = io.BytesIO()
            doc.save(doc_stream)
            doc_stream.seek(0)

            # Encode the document in base64
            encoded_file = base64.b64encode(doc_stream.read()).decode('utf-8')

            # Upload document to Firestore
            file_data = {
                "file_name": "text_input_submission.docx",
                "file_content": encoded_file,
            }
            db.collection("N4KFORMW").add(file_data)
            st.success("Document uploaded successfully!")

        except Exception as e:
            st.error(f"An error occurred while submitting the form: {e}")

# Streamlit app layout
def main():
    initialize_firebase()
    get_firestore()

    st.header("Simple Firestore Document Upload")

    text_input = st.text_area("Enter your text here:")
    
    if text_input:
        submit_form(text_input)

if __name__ == "__main__":
    main()
