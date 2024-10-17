import streamlit as st
import re
from docx import Document

def extract_date(text):
    # Regex to find the date following "Date:"
    match = re.search(r'Date:\s*(.*)', text)
    if match:
        return match.group(1).strip()
    return None

def replace_placeholder(doc_path, placeholder, value):
    doc = Document(doc_path)
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, value)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if placeholder in cell.text:
                    cell.text = cell.text.replace(placeholder, value)

    return doc

# Streamlit UI
st.title("N4K")

input_text = st.text_area("Paste your text here:")

if st.button("Extract Date and Replace Placeholder"):
    date_value = extract_date(input_text)
    
    if date_value:
        placeholder = "{date_placeholder}"  # Replace with your actual placeholder
        doc_path = "ndcf.docx"  # Replace with your document path
        
        # Replace placeholder in the document
        modified_doc = replace_placeholder(doc_path, placeholder, date_value)
        
        # Save the modified document
        modified_doc.save("modified_document.docx")
        
        st.success("Date extracted and placeholder replaced!")
        st.download_button("Download modified document", "modified_document.docx")
    else:
        st.error("No date found in the input text.")
