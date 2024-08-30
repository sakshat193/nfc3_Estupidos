import streamlit as st
from sqlalchemy.orm import Session
from models import SessionLocal, User, init_db
import time
import random

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

def generate_svg_shapes(num_shapes):
    svg_code = ""
    for _ in range(num_shapes):
        shape_size = random.randint(50, 200)
        blur_level = shape_size / 100
        shape_color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, {random.random()})"
        shape_type = random.choice(["circle", "rect", "ellipse"])
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        if shape_type == "circle":
            svg_code += f'<circle cx="{x}%" cy="{y}%" r="{shape_size}" fill="{shape_color}" filter="blur({blur_level}px)"/>'
        elif shape_type == "rect":
            svg_code += f'<rect x="{x}%" y="{y}%" width="{shape_size}" height="{shape_size}" fill="{shape_color}" filter="blur({blur_level}px)"/>'
        elif shape_type == "ellipse":
            svg_code += f'<ellipse cx="{x}%" cy="{y}%" rx="{shape_size}" ry="{shape_size/2}" fill="{shape_color}" filter="blur({blur_level}px)"/>'
    return svg_code

# Generate random SVG shapes
num_shapes = 20
svg_code = generate_svg_shapes(num_shapes)

# Write SVG code to the page
st.write(f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='100%' height='100%' style='position: absolute; top: 0; left: 0; z-index: -1'>
    {svg_code}
    </svg>
""", unsafe_allow_html=True)

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
                        st.switch_page('pages/Landing-Page.py')
                    else:
                        st.error("Incorrect password. Please try again.")
                else:
                    st.error("User not found.")
    else:
        st.error("Please fill all the fields.")