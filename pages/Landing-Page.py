import streamlit as st
import os

# Set page config at the very beginning
st.set_page_config(page_title="Personal Finance Platform", initial_sidebar_state="collapsed")

# Function to load CSS
def load_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS from the correct path
css_path = os.path.join('static', 'css', 'style.css')
load_css(css_path)

# Add vector designs using inline SVG
st.markdown("""
    <div class="vector-container">
        <svg class="vector vector-1" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" />
        </svg>
        <svg class="vector vector-2" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" />
        </svg>
        <svg class="vector vector-3" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" />
        </svg>
        <svg class="vector vector-4" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" />
        </svg>
        <svg class="vector vector-5" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <circle cx="100" cy="100" r="100" />
        </svg>
    </div>
""", unsafe_allow_html=True)

main_container = st.container()

with main_container:
    # Add hero section
    st.markdown("""
    <div class="hero">
        <h1>Personal Finance Platform</h1>
        <p>Take control of your financial future</p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for buttons
    col1, col2 = st.columns((1, 1))

    # Button 1: PFM Management
    with col1:
        if st.button("Personal Finance", key="pfm_button", use_container_width=True):
            st.switch_page("pages/Expense_Record.py")

    # Button 2: Stock Market Investment
    with col2:
        if st.button("Stock Market Investment", key="stock_button", use_container_width=True):
            st.switch_page("pages/Stock_Management.py")

    # Add features section
    st.markdown("""
    <div class="features">
        <h2>Our Features</h2>
        <div class="feature-grid">
            <div class="feature-item">
                <h3>Expense Tracking</h3>
                <p>Monitor and categorize your spending effortlessly.</p>
            </div>
            <div class="feature-item">
                <h3>Budgeting Tools</h3>
                <p>Plan and track your budget efficiently.</p>
            </div>
            <div class="feature-item">
                <h3>Savings Goal Setting</h3>
                <p>Set and achieve your savings goals.</p>
            </div>
            <div class="feature-item">
                <h3>Debt Management</h3>
                <p>Manage and reduce your debts effectively.</p>
            </div>
            <div class="feature-item">
                <h3>Portfolio Optimization</h3>
                <p>Optimize your investment portfolio.</p>
            </div>
            <div class="feature-item">
                <h3>Real-Time Investment Support</h3>
                <p>Receive real-time insights and recommendations.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigate")
nav = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

if nav == "About":
    st.markdown("""
    <div class="about">
        <h2>About Us</h2>
        <p>Our platform is designed to enhance personal finance management and optimize stock market investment strategies. We focus on delivering personalized recommendations and analyzing extensive datasets to help you make informed financial decisions.</p>
    </div>
    """, unsafe_allow_html=True)

elif nav == "Contact":
    st.markdown("""
    <div class="contact">
        <h2>Contact Us</h2>
        <p>If you have any questions or need support, please reach out to us:</p>
        <ul>
            <li><strong>Email:</strong> example_email@gmail.com</li>
            <li><strong>Phone:</strong> +91 12345 67890</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Add footer
st.markdown("""
<footer>
    <p>&copy; 2023 Personal Finance Platform. All rights reserved.</p>
</footer>
""", unsafe_allow_html=True)

st.write("""
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
