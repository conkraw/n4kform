import streamlit as st
import re
from docx import Document
from io import BytesIO

def extract_date(text):
    match = re.search(r'Date:\s*(.*)', text)
    if match:
        return match.group(1).strip()
    return None

def replace_placeholder(doc_path, placeholder, value):
    value = value.rstrip('.')  # Remove any trailing periods from the value
    doc = Document(doc_path)

    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            # Replace placeholder with underlined text
            for run in paragraph.runs:
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, value)
                    run.underline = True  # Underline the replaced text

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if placeholder in cell.text:
                    # Replace placeholder with underlined text in cell
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            if placeholder in run.text:
                                run.text = run.text.replace(placeholder, value)
                                run.underline = True  # Underline the replaced text

    return doc

st.title("Date Placeholder Replacer")

input_text = st.text_area("Paste your text here:")

if st.button("Extract Date and Replace Placeholder"):
    date_value = extract_date(input_text)
    
    if date_value:
        placeholder = "{date_placeholder}"  # Your placeholder
        doc_path = "ndcf.docx"  # Your document path
        
        modified_doc = replace_placeholder(doc_path, placeholder, date_value)
        
        doc_stream = BytesIO()
        modified_doc.save(doc_stream)
        doc_stream.seek(0)

        st.success("Date extracted and placeholder replaced!")
        
        st.download_button(
            label="Download modified document",
            data=doc_stream,
            file_name="modified_document.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("No date found in the input text.")


