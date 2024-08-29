import streamlit as st
import base64
from PIL import Image

# Set up the page configuration
st.set_page_config(page_title="DAAM DOST Login", page_icon="Untitled design.png")

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

# logo = Image.open("logo.png")
# st.image(logo, width=150)

# Page Title
st.title("DAAM DOST - Finance Manager Login")

# Form fields
name = st.text_input("Name", placeholder="Enter your name")
password = st.text_input("Password", type="password", placeholder="Enter your password")
mobile_number = st.text_input("Mobile Number", placeholder="Enter your mobile number")

# OTP placeholder and Login button
if st.button("Send OTP"):
    if name and password and mobile_number:
        st.session_state['name'] = name
        st.session_state['password'] = password
        st.session_state['otp'] = 1234  # Setting OTP to 1234 for simplicity
        st.success(f"OTP 1234 sent to {mobile_number}")
    else:
        st.error("Please fill in all fields.")

if 'otp' in st.session_state:
    input_otp = st.text_input("Enter OTP", placeholder="Enter the OTP sent to your mobile", type="password")

    if st.button("Login"):
        if input_otp == str(st.session_state['otp']) and password == st.session_state['password']:
            st.success(f"Welcome, {name}! You're now logged in.")
        else:
            st.error("Incorrect OTP or Password. Please try again.")
