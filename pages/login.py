import streamlit as st
import base64
from sqlalchemy.orm import Session
from models import SessionLocal, User, init_db

# Set up the page configuration
st.set_page_config(page_title="DAAM DOST Login", page_icon="Untitled design.png")
init_db()
# Set background image using CSS
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background color and style
set_background('Colorful Simple Illustrative Finance Presentation (2).jpg')

# Page Title
st.title("DAAM DOST - Finance Manager Login")

# Form fields
name = st.text_input("Name", placeholder="Enter your name")
password = st.text_input("Password", type="password", placeholder="Enter your password")
mobile_number = st.text_input("Mobile Number", placeholder="Enter your mobile number")

def get_user(session: Session, name: str, mobile_number: str):
    return session.query(User).filter_by(username=name, mobile_number=mobile_number).first()

if st.button("Login"):
    if name and password and mobile_number:
        with SessionLocal() as session:
            if len(mobile_number) != 10 or not mobile_number.isdigit():
                st.error("Please enter a valid mobile number with 10 digits.")
            else:
                user = get_user(session, name, mobile_number)
                if user:
                    if user.password == password:
                        st.success(f"Welcome, {name}! You're now logged in.")
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("User not found.")
    else:
        st.error("Please fill all the fields.")