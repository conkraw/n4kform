import streamlit as st
import re
from docx import Document
from io import BytesIO

def extract_info(text):
    date_match = re.search(r'Date:\s*(.*)', text)
    time_match = re.search(r'Time:\s*(.*)', text)
    performed_by_match = re.search(r'Performed by:\s*(.*)', text)
    supervised_match = re.search(r'Present and supervised procedure:\s*(.*)', text)
    
    date_value = date_match.group(1).strip() if date_match else None
    time_value = time_match.group(1).strip() if time_match else ""  # Set to empty string if not found
    performed_by_value = performed_by_match.group(1).strip() if performed_by_match else None
    attending_value = "YES" if supervised_match and supervised_match.group(1).strip() else "NO"
    
    return date_value, time_value, performed_by_value, attending_value

def replace_placeholder(doc_path, date_placeholder, date_value, time_placeholder, time_value, performed_by_placeholder, performed_by_value, attending_placeholder, attending_value):
    date_value = date_value.rstrip('.') if date_value else ""
    time_value = time_value.rstrip('.') if time_value else ""  # Ensure it’s empty if not found
    performed_by_value = performed_by_value.rstrip('.') if performed_by_value else ""
    
#def replace_placeholder(doc_path, date_placeholder, date_value, time_placeholder, time_value, performed_by_placeholder, performed_by_value, attending_placeholder, attending_value):
    doc = Document(doc_path)

    # Function to replace placeholders in runs
    def replace_in_runs(runs, placeholder, value):
        for run in runs:
            if placeholder in run.text:
                run.text = run.text.replace(placeholder, value)
                run.underline = True

    # Replace in paragraphs
    for paragraph in doc.paragraphs:
        replace_in_runs(paragraph.runs, date_placeholder, date_value)
        replace_in_runs(paragraph.runs, time_placeholder, time_value)
        replace_in_runs(paragraph.runs, performed_by_placeholder, performed_by_value)
        replace_in_runs(paragraph.runs, attending_placeholder, attending_value)

    # Replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_runs(paragraph.runs, date_placeholder, date_value)
                    replace_in_runs(paragraph.runs, time_placeholder, time_value)
                    replace_in_runs(paragraph.runs, performed_by_placeholder, performed_by_value)
                    replace_in_runs(paragraph.runs, attending_placeholder, attending_value)

    return doc


st.title("Date, Time, Performer, and Attending Placeholder Replacer")

input_text = st.text_area("Paste your text here:")

if st.button("Extract and Replace Placeholders"):
    date_value, time_value, performed_by_value, attending_value = extract_info(input_text)
    
    if date_value or time_value or performed_by_value or attending_value:
        date_placeholder = "{date_placeholder}"
        time_placeholder = "{time_placeholder}"
        performed_by_placeholder = "{performed_by_placeholder}"
        attending_placeholder = "{attending_placeholder}"
        doc_path = "nqf.docx"  # Your document path
        
        modified_doc = replace_placeholder(doc_path, date_placeholder, date_value, time_placeholder, time_value, performed_by_placeholder, performed_by_value, attending_placeholder, attending_value)
        
        doc_stream = BytesIO()
        modified_doc.save(doc_stream)
        doc_stream.seek(0)

        st.success("Placeholders extracted and replaced!")
        
        st.download_button(
            label="Download modified document",
            data=doc_stream,
            file_name="modified_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("No relevant information found in the input text.")


