import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd

# Set page title and icon
st.set_page_config(page_title="Company Stock Data Viewer", page_icon=":moneybag:", layout="wide")

if st.button("Back to Home"):
    st.switch_page("pages/Landing-Page.py")

# Title and description
st.title("Company Stock Data Viewer")
st.write("Select a company and view its stock data over a specified time span.")

# Sidebar for user inputs
st.sidebar.title("Select Options")

# Create a dictionary of Sensex companies and their ticker symbols
sensex_companies = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "Hindustan Unilever": "HINDUNILVR.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Kotak Mahindra Bank": "KOTAKBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Bajaj Finance": "BAJFINANCE.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Asian Paints": "ASIANPAINT.NS",
    "Maruti Suzuki": "MARUTI.NS",
    "Larsen & Toubro": "LT.NS",
    "Axis Bank": "AXISBANK.NS",
    "ITC": "ITC.NS",
    "HCL Technologies": "HCLTECH.NS",
    "UltraTech Cement": "ULTRACEMCO.NS",
    "Mahindra & Mahindra": "M&M.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Power Grid Corporation": "POWERGRID.NS",
    "Nestle India": "NESTLEIND.NS",
    "Wipro": "WIPRO.NS",
    "Titan Company": "TITAN.NS",
    "Sun Pharma": "SUNPHARMA.NS",
    "NTPC": "NTPC.NS",
    "Bajaj Auto": "BAJAJ-AUTO.NS",
    "IndusInd Bank": "INDUSINDBK.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Tech Mahindra": "TECHM.NS",
    "Hindalco Industries": "HINDALCO.NS",
    "JSW Steel": "JSWSTEEL.NS",
    "Grasim Industries": "GRASIM.NS",
    "Eicher Motors": "EICHERMOT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Dr. Reddy's Laboratories": "DRREDDY.NS",
    "Tata Consumer Products": "TATACONSUM.NS",
    "SBI Life Insurance": "SBILIFE.NS",
    "Bharat Petroleum": "BPCL.NS",
    "HDFC Life Insurance": "HDFCLIFE.NS",
    "Divi's Laboratories": "DIVISLAB.NS",
    "UPL": "UPL.NS",
    "Shree Cement": "SHREECEM.NS",
    "Cipla": "CIPLA.NS",
    "ONGC": "ONGC.NS",
    "Hero MotoCorp": "HEROMOTOCO.NS",
    "Britannia Industries": "BRITANNIA.NS",
    "Coal India": "COALINDIA.NS",
    "Tata Power": "TATAPOWER.NS",
    "Zee Entertainment": "ZEEL.NS",
    "GAIL India": "GAIL.NS",
    "Godrej Consumer Products": "GODREJCP.NS",
    "DLF": "DLF.NS"
}

# Dropdown for stock ticker symbol
company = st.sidebar.selectbox("Select Stock Ticker Symbol", list(sensex_companies.keys()))

time_span = st.sidebar.selectbox("Select Time Span", ["5 days", "1 month", "3 months", "6 months", "1 year", "5 years"])
graph_type = st.sidebar.selectbox("Select Graph Type", ["Line", "Candlestick", "Bar"])

# Get historical data based on time span
if time_span == "5 days":
    period = "5d"
elif time_span == "1 month":
    period = "1mo"
elif time_span == "3 months":
    period = "3mo"
elif time_span == "6 months":
    period = "6mo"
elif time_span == "1 year":
    period = "1y"
else:
    period = "5y"

# Fetch data from yfinance
stock_data = yf.Ticker(sensex_companies[company])
df = stock_data.history(period=period)

# Remove timezone information
df.index = df.index.tz_localize(None)

# Plotting the selected graph
if graph_type == "Line":
    fig = go.Figure(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=company))
elif graph_type == "Candlestick":
    fig = go.Figure(go.Candlestick(x=df.index,
                                   open=df['Open'],
                                   high=df['High'],
                                   low=df['Low'],
                                   close=df['Close'],
                                   name=company))
elif graph_type == "Bar":
    fig = go.Figure(go.Bar(x=df.index, y=df['Close'], name=company))

# Set graph layout
fig.update_layout(title=f"{company} Stock Price ({time_span})",
                  xaxis_title="Date",
                  yaxis_title="Price (INR)",
                  xaxis_rangeslider_visible=False)

# Display the plot
st.plotly_chart(fig)

# Forecast section
st.subheader("Stock Price Forecast")

# User input for forecast days
forecast_days = st.number_input("Number of days to forecast", min_value=1, max_value=365, value=30)

# Prepare data for Prophet
df_prophet = df.reset_index()[['Date', 'Close']]
df_prophet.columns = ['ds', 'y']

# Create and fit the model
model = Prophet()
model.fit(df_prophet)

# Create future dataframe
future = model.make_future_dataframe(periods=forecast_days)

# Make predictions
forecast = model.predict(future)

# Plot the forecast
fig_forecast = plot_plotly(model, forecast)
fig_forecast.update_layout(title=f"{company} Stock Price Forecast (Next {forecast_days} days)",
                           xaxis_title="Date",
                           yaxis_title="Price (INR)")

# Display the forecast plot
st.plotly_chart(fig_forecast)

st.write("""
<style>
/* Light mode background and text color */
body {
    background-color: #ffffff;
    color: #000000;
}""", unsafe_allow_html=True)

# Display raw data
st.subheader("Stock Data")
st.write(df)