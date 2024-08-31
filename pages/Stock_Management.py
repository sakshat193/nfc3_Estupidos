import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Assuming you store the key in st.secrets
google_api_key = st.secrets["google"]["api_key"]

# Check if the API key is available
if not google_api_key:
    st.error("Google API key not found. Please check your Streamlit secrets configuration.")
    st.stop()

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

# Function to generate insights using Langchain and Gemini
def generate_insights(company, forecast_data, historical_data):
    # Create an instance of the Gemini Pro model
    llm = ChatGoogleGenerativeAI(api_key=google_api_key, model="gemini-pro", temperature=0.7)

    # Create a prompt template
    template = """
    You are a financial analyst. Based on the following data for {company}, provide insights and analysis:

    Historical data summary:
    Start date: {hist_start}
    End date: {hist_end}
    Starting price: {hist_start_price}
    Ending price: {hist_end_price}
    Highest price: {hist_max_price}
    Lowest price: {hist_min_price}

    Forecast data summary:
    Forecast start: {forecast_start}
    Forecast end: {forecast_end}
    Forecasted start price: {forecast_start_price}
    Forecasted end price: {forecast_end_price}
    Highest forecasted price: {forecast_max_price}
    Lowest forecasted price: {forecast_min_price}

    Please provide:
    1. A brief overview of the historical performance
    2. Key trends observed in the forecast
    3. Potential factors that might influence the stock price
    4. Any risks or opportunities for investors
    5. A concise conclusion

    Limit your response to about 150 words.
    """

    # Create a prompt from the template
    prompt = PromptTemplate(
        input_variables=["company", "hist_start", "hist_end", "hist_start_price", "hist_end_price", "hist_max_price", "hist_min_price",
                         "forecast_start", "forecast_end", "forecast_start_price", "forecast_end_price", "forecast_max_price", "forecast_min_price"],
        template=template
    )

    # Create a chain
    chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain
    insights = chain.run(
        company=company,
        hist_start=historical_data.index[0].date(),
        hist_end=historical_data.index[-1].date(),
        hist_start_price=round(historical_data['Close'].iloc[0], 2),
        hist_end_price=round(historical_data['Close'].iloc[-1], 2),
        hist_max_price=round(historical_data['Close'].max(), 2),
        hist_min_price=round(historical_data['Close'].min(), 2),
        forecast_start=forecast_data['ds'].iloc[-forecast_days].date(),
        forecast_end=forecast_data['ds'].iloc[-1].date(),
        forecast_start_price=round(forecast_data['yhat'].iloc[-forecast_days], 2),
        forecast_end_price=round(forecast_data['yhat'].iloc[-1], 2),
        forecast_max_price=round(forecast_data['yhat'].tail(forecast_days).max(), 2),
        forecast_min_price=round(forecast_data['yhat'].tail(forecast_days).min(), 2)
    )

    return insights

# Button to generate insights
if st.button("Generate Insights"):
    with st.spinner("Generating insights..."):
        insights = generate_insights(company, forecast, df)
        st.subheader("AI-Generated Insights")
        st.write(insights)

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


# Display raw data
st.subheader("Stock Data")
st.write(df)