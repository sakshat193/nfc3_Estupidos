import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import os

# Page configuration
st.set_page_config(page_title="Daam-Dost", page_icon=":moneybag:")

if st.button("Back to Home"):
    st.switch_page("pages/Landing-Page.py")

# File to store the expenses data
DATA_FILE = 'expenses.csv'

# Function to load data from CSV file
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame(columns=['Date', 'Amount'])

# Function to save data to CSV file
def save_data(df):
    df_to_save = df.copy()
    df_to_save['Date'] = df_to_save['Date'].astype(str)
    df_to_save.to_csv(DATA_FILE, index=False)

# Load the data
if 'expenses' not in st.session_state:
    st.session_state.expenses = load_data()

st.title('Expense Tracker')

# Input fields
input_date = st.date_input('Date')
amount = st.number_input('Amount Spent', min_value=0, step=1)

if st.button('Add Expense'):
    # Check if the new entry is not earlier than the most recent entry
    if not st.session_state.expenses.empty:
        last_date = st.session_state.expenses['Date'].max()
        if input_date < last_date:
            st.error(f'Error: The new entry date ({input_date}) must not be earlier than the most recent entry ({last_date}).')
        else:
            # Proceed with adding/updating the expense
            if input_date in st.session_state.expenses['Date'].values:
                # If exists, update the amount
                st.session_state.expenses.loc[st.session_state.expenses['Date'] == input_date, 'Amount'] += amount
            else:
                # If not, add a new row
                new_expense = pd.DataFrame({'Date': [input_date], 'Amount': [amount]})
                st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
            
            # Sort the DataFrame by date
            st.session_state.expenses = st.session_state.expenses.sort_values('Date')
            
            # Save the updated DataFrame
            save_data(st.session_state.expenses)
            
            st.success('Expense added successfully!')
    else:
        # If it's the first entry, add it without checks
        new_expense = pd.DataFrame({'Date': [input_date], 'Amount': [amount]})
        st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
        save_data(st.session_state.expenses)
        st.success('Expense added successfully!')

# Display the data
st.subheader('Recorded Expenses')
st.dataframe(st.session_state.expenses)

# Create and display the Plotly graph
if not st.session_state.expenses.empty:
    fig = px.line(st.session_state.expenses, x='Date', y='Amount', title='Daily Expenses Over Time')
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Amount Spent',
        xaxis=dict(
            tickmode='array',
            tickvals=st.session_state.expenses['Date'],
            ticktext=[d.strftime('%Y-%m-%d') for d in st.session_state.expenses['Date']],
            tickangle=45
        )
    )
    st.plotly_chart(fig)
else:
    st.info('No expenses recorded yet. Add some expenses to see the graph!')

if st.sidebar.button('Upload Bank Statement'):
    page = 'pages/Upload-Bank-Statement.py'
    st.write("Redirecting to Back Statement page...")
    st.switch_page(page)