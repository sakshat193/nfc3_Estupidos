import streamlit as st
import pandas as pd
import plotly.express as px

def preprocess_data(df):
    """
    Preprocess the data by converting the Date column to datetime, 
    filling missing values in Withdrawals and Deposits columns, 
    and calculating the Savings and Month columns.
    """
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Withdrawals"].fillna(0, inplace=True)
    df["Deposits"].fillna(0, inplace=True)
    
    df["Month"] = df["Date"].dt.to_period("M").dt.strftime("%Y-%m")
    df["Savings"] = df["Deposits"] - df["Withdrawals"]
    
    monthly_summary = df.groupby("Month").agg({
        "Withdrawals": "sum",
        "Deposits": "sum",
        "Savings": "sum"
    }).reset_index()
    
    # Calculate percentage change in savings compared to the previous month
    monthly_summary["Previous Savings"] = monthly_summary["Savings"].shift(1)
    monthly_summary["Savings Change (%)"] = (
        (monthly_summary["Savings"] - monthly_summary["Previous Savings"]) / monthly_summary["Previous Savings"] * 100
    ).fillna(0)
    
    return monthly_summary

def predict_monthly_income(monthly_summary):
    """
    Predict the next month's income as the average of the last N months
    """
    N = 3  # You can adjust this value to use more or fewer months for the prediction
    avg_monthly_income = monthly_summary["Deposits"].tail(N).mean()
    
    return avg_monthly_income

def main():
    st.set_page_config(page_title="Bank Statement Analyzer", page_icon=":moneybag:")
    st.write("<a href='/'><img src='https://img.icons8.com/ios/24/000000/home--v1.png' width='24' height='24' alt='Home' style='margin: 0 10px;'></a>", unsafe_allow_html=True)
    st.title("Bank Statement Analyzer")
    st.markdown("Upload your bank statement (Excel file) to analyze your monthly expenditure, income, and savings.")

    
    uploaded_file = st.file_uploader("", type=["xls", "xlsx"], key="file_uploader")
    
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        monthly_summary = preprocess_data(df)
        
        # Plot using Plotly
        fig = px.bar(monthly_summary, x="Month", y=["Withdrawals", "Deposits", "Savings"],
                     title="Monthly Expenditure, Income, and Savings", barmode="group",
                     labels={"value": "Amount (INR)", "variable": "Category"})
        fig.update_layout(xaxis_title="Month", yaxis_title="Amount (INR)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the table with percentage change in savings
        st.header("Percentage Change in Savings Compared to Last Month")
        st.write(monthly_summary[["Month", "Savings Change (%)"]].style.format({"Savings Change (%)": "{:.2f}%"}))
        
        # Predict and display the next month's income
        predicted_income = predict_monthly_income(monthly_summary)
        st.header("Predicted Average Monthly Income")
        st.success(f"₹{predicted_income:.2f}")
        
        st.markdown("---")
        # st.write("Note: The predicted income is based on the average of the last 3 months' income. You can adjust this value by changing the `N` parameter in the `predict_monthly_income` function.")

if __name__ == "__main__":
    main()