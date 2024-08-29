import streamlit as st

# Set page title, icon, and layout
st.set_page_config(page_title="Daam-Dost", page_icon=":moneybag:", layout="wide")

# Welcome message
st.title("Daam-Dost")
st.write("Save. Spend. Succeed.")

# Create two columns for buttons
col1, col2 = st.columns(2)

# Button 1: PFM Management
with col1:
    if st.button("PFM Management", key="pfm_button"):
        st.write("Redirecting to PFM Management page...")
        # Redirect to pfm_app.py
        st.query_params.update({"app": "pfm"})

# Button 2: Stock Market Investment
with col2:
    if st.button("Stock Market Investment", key="stock_button"):
        st.write("Redirecting to Stock Market Investment page...")
        # Redirect to Stock-Management.py
        st.switch_page("pages\📈Stock-Management.py")

# Custom CSS for light mode and button animations
st.write("""
<style>
/* Light mode background and text color */
body {
    background-color: #ffffff;
    color: #000000;
}

/* Enhance grow and glow animation */
button:hover {
    transform: scale(1.15);
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    background-color: #FFFFFF;
    color: #FFFFFF;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
</style>
""", unsafe_allow_html=True)