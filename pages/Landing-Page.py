import streamlit as st
import base64

st.set_page_config(page_title="Personal Finance Platform", layout="wide")

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

set_background('Colorful Simple Illustrative Finance Presentation (2).jpg')

if "nav" not in st.session_state:
    st.session_state.nav = "About"

def set_nav(new_nav):
    st.session_state.nav = new_nav

st.sidebar.title("Navigate")
if st.sidebar.button("About"):
    set_nav("About")
if st.sidebar.button("Features"):
    set_nav("Features")
if st.sidebar.button("Contact Me"):
    set_nav("ContactMe")

if st.session_state.nav == "About":
    st.subheader("About Us")
    st.write(
        """
        Our platform is designed to enhance personal finance management and optimize stock market investment strategies. Leveraging AI-driven capabilities, we provide tools for:
        - Expense Tracking
        - Budgeting
        - Savings Goal Setting
        - Debt Management
        - Portfolio Optimization
        - Real-Time Investment Decision Support

        We focus on delivering personalized recommendations and analyzing extensive datasets to help you make informed financial decisions.
        """
    )

elif st.session_state.nav == "Features":
    st.subheader("Features")
    st.write(
        """
        **Expense Tracking**: Monitor and categorize your spending.

        **Budgeting Tools**: Plan and track your budget efficiently.

        **Savings Goal Setting**: Set and achieve your savings goals.

        **Debt Management**: Manage and reduce your debts effectively.

        **Portfolio Optimization**: Optimize your investment portfolio.

        **Real-Time Investment Decision Support**: Receive real-time insights and recommendations.
        """
    )

elif st.session_state.nav == "ContactMe":
    st.subheader("Contact Us")
    st.write(
        """
        If you have any questions or need support, please reach out to us:
        
        - **Email**: example_email@gmail.com
        - **Phone**: +91 12345 67890
        """
    )
