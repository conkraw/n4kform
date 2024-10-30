import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

# Function to send email
def send_email(to_email, subject, body):
    from_email = st.secrets["general"]["email_user"]
    password = st.secrets["general"]["email_password"]

    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))
    
    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:  # Use SMTP_SSL for port 465
            server.login(from_email, password)
            server.send_message(msg)
            st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Streamlit app
st.title("Email Sender")

text_input = st.text_area("Enter your message here:")
recipient_email = st.text_input("Enter recipient email:")
subject = st.text_input("Enter email subject:")

if st.button("Send Email"):
    if text_input and recipient_email and subject:
        send_email(recipient_email, subject, text_input)
    else:
        st.error("Please fill in all fields.")

