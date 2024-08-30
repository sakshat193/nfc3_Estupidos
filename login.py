import streamlit as st
from sqlalchemy.orm import Session
from models import SessionLocal, User, init_db
import time

# Set up the page configuration
st.set_page_config(page_title="DAAM DOST Login")
init_db()

# Page Title
st.title("DAAM DOST - Finance Manager Login")

# Form fields
name = st.text_input("Username", placeholder="Enter your username")
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
                        st.session_state.logged_in = True  # Set login state
                        time.sleep(2)                        
                        st.switch_page('pages\Landing-Page.py')
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("User not found.")
    else:
        st.error("Please fill all the fields.")
