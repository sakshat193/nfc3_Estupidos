import streamlit as st
import base64

st.set_page_config(page_title="Personal Finance Platform", layout="wide")

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

# Add a new section for the buttons
st.write("""
<h1 style="font-size: 36px; font-weight: bold; color: #FFFFFF; text-align: left; margin-left: 20px;">
    <span style="border-radius: 10px; padding: 10px; background-color: #0E1117; transition: background-color 0.3s ease, transform 0.3s ease;">
        Get Started
    </span>
</h1>
""", unsafe_allow_html=True)

st.write("Explore our features and start managing your finances today!")
st.write("")

# Create two columns for buttons
col1, col2 = st.columns((1, 1))  # Adjust the column widths to make the buttons closer

# Add some CSS to make the "Get Started" text grow on hover
st.write("""
<style>
    h1 span:hover {
        transform: scale(1.1);
        background-color: #333;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Button 1: PFM Management
with col1:
    if st.button("Personal Finance", key="pfm_button"):
        st.write("Redirecting to PFM Management page...")
        # Redirect to pfm_app.py
        st.switch_page("pages\Expense_Record.py")

# Button 2: Stock Market Investment
with col2:
    if st.button("Stock Market Investment", key="stock_button"):
        st.write("Redirecting to Stock Market Investment page...")
        # Redirect to Stock-Management.py
        st.switch_page("pages\Stock_Management.py")

        
st.write("""
<style>
/* Dark mode background and text color */
body {
    background-color: #0E1117;
    color: #ffffff;
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

