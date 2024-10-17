import streamlit as st
import re
from docx import Document
from io import BytesIO

def extract_info(text):
    date_match = re.search(r'Date:\s*(.*)', text)
    time_match = re.search(r'Time:\s*(.*)', text)
    date_value = date_match.group(1).strip() if date_match else None
    time_value = time_match.group(1).strip() if time_match else None
    return date_value, time_value

def replace_placeholder(doc_path, date_placeholder, date_value, time_placeholder, time_value):
    date_value = date_value.rstrip('.') if date_value else ""
    time_value = time_value.rstrip('.') if time_value else ""
    doc = Document(doc_path)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if date_placeholder in run.text:
                run.text = run.text.replace(date_placeholder, date_value)
                run.underline = True  # Underline the replaced text
            if time_placeholder in run.text:
                run.text = run.text.replace(time_placeholder, time_value)
                run.underline = True  # Underline the replaced text

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if date_placeholder in run.text:
                            run.text = run.text.replace(date_placeholder, date_value)
                            run.underline = True  # Underline the replaced text
                        if time_placeholder in run.text:
                            run.text = run.text.replace(time_placeholder, time_value)
                            run.underline = True  # Underline the replaced text

    return doc

st.title("Date and Time Placeholder Replacer")

input_text = st.text_area("Paste your text here:")

if st.button("Extract Date and Time and Replace Placeholders"):
    date_value, time_value = extract_info(input_text)
    
    if date_value or time_value:
        date_placeholder = "{date_placeholder}"  # Your date placeholder
        time_placeholder = "{time_placeholder}"  # Your time placeholder
        doc_path = "ndcf.docx"  # Your document path
        
        modified_doc = replace_placeholder(doc_path, date_placeholder, date_value, time_placeholder, time_value)
        
        doc_stream = BytesIO()
        modified_doc.save(doc_stream)
        doc_stream.seek(0)

        st.success("Date and/or Time extracted and placeholders replaced!")
        
        st.download_button(
            label="Download modified document",
            data=doc_stream,
            file_name="modified_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("No date or time found in the input text.")


