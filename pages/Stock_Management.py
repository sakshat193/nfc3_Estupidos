import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd
import os
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

# Assuming you store the key in st.secrets
google_api_key = st.secrets["google"]["api_key"]

# Check if the API key is available
if not google_api_key:
    st.error("Google API key not found. Please check your Streamlit secrets configuration.")
    st.stop()

# Configure the Gemini API
try:
    genai.configure(api_key=google_api_key)
except Exception:
    # Older clients may not expose configure; fall back to env var
    os.environ["GOOGLE_API_KEY"] = google_api_key

def _pick_supported_model():
    """Probe candidate model names until one works, then cache it.

    This avoids SDK/API version mismatches (v1 vs v1beta) and 404s.
    """
    if "genai_working_model" in st.session_state:
        return st.session_state["genai_working_model"]

    candidates = [
        # Prefer fully-qualified names first
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-1.0-pro",
        # 1.5 latest aliases
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-pro-latest",
        # 1.5 8B variants where available
        "models/gemini-1.5-flash-8b",
        "models/gemini-1.5-pro-8b",
        # Short names (some SDKs accept these)
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.0-pro",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro-8b",
        # Fallback to PaLM2 if Gemini not available
        "models/text-bison-001",
        "text-bison-001",
    ]

    model_ctor = getattr(genai, "GenerativeModel", None)
    for name in candidates:
        try:
            # Tiny probe to confirm availability without spending much
            if model_ctor:
                model = model_ctor(name)
                resp = model.generate_content("ok", request_options={"timeout": 8})
                ok_text = getattr(resp, "text", None)
            else:
                # Legacy fallback API
                gen_text = getattr(genai, "generate_text", None)
                if gen_text:
                    resp = gen_text(model=name, prompt="ok")
                    ok_text = getattr(resp, "result", None) or getattr(resp, "candidates", [None])[0]
                else:
                    ok_text = None
            if ok_text is not None:
                st.session_state["genai_working_model"] = name
                return name
        except google_exceptions.NotFound:
            continue
        except Exception:
            # Ignore and try next candidate; other errors may be perms/timeouts
            continue
    return None


# Allow user to override the model preference via UI
KNOWN_MODEL_CANDIDATES = [
    "Auto (recommended)",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-pro",
    "models/gemini-1.0-pro",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-pro-latest",
    "models/gemini-1.5-flash-8b",
    "models/gemini-1.5-pro-8b",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro-8b",
    "models/text-bison-001",
    "text-bison-001",
]

def _normalize_model_name(name: str) -> str:
    # Prefer fully qualified name; API accepts both in many cases
    if name.startswith("models/"):
        return name
    return f"models/{name}"

# Sidebar model override
st.sidebar.markdown("---")
override = st.sidebar.selectbox("Model (optional)", options=KNOWN_MODEL_CANDIDATES, index=0)
if override != "Auto (recommended)":
    st.session_state["genai_working_model"] = _normalize_model_name(override)

# Show which model is selected
resolved = _pick_supported_model()
st.sidebar.caption(f"Using model: {resolved or 'unresolved'}")

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

# Function to generate insights using Google Gemini
def _generate_with_model(model_name: str, prompt: str) -> str:
    """Generate text using either new or legacy google-generativeai client APIs."""
    model_ctor = getattr(genai, "GenerativeModel", None)
    if model_ctor:
        model = model_ctor(model_name)
        response = model.generate_content(prompt)
        return getattr(response, "text", "") or ""
    # Legacy fallback
    gen_text = getattr(genai, "generate_text", None)
    if gen_text:
        resp = gen_text(model=model_name, prompt=prompt)
        # Try typical legacy response shapes
        if hasattr(resp, "result") and resp.result:
            return resp.result
        if hasattr(resp, "candidates") and resp.candidates:
            cand = resp.candidates[0]
            # Some versions use dicts, others objects
            if isinstance(cand, dict):
                return cand.get("output", "")
            return getattr(cand, "output", "")
    raise RuntimeError("No compatible generation method available in google-generativeai client.")


def generate_insights(company, forecast_data, historical_data):
    # Resolve a working model name
    model_name = _pick_supported_model()
    if not model_name:
        st.error("No supported text generation model is available for this API key/region. Enable Gemini models in Google AI Studio and try again.")
        return "AI model unavailable at the moment. Please try again later."

    # Create the prompt
    prompt = f"""
    You are a financial analyst. Based on the following data for {company}, provide insights and analysis:

    Historical data summary:
    Start date: {historical_data.index[0].date()}
    End date: {historical_data.index[-1].date()}
    Starting price: ${round(historical_data['Close'].iloc[0], 2)}
    Ending price: ${round(historical_data['Close'].iloc[-1], 2)}
    Highest price: ${round(historical_data['Close'].max(), 2)}
    Lowest price: ${round(historical_data['Close'].min(), 2)}

    Forecast data summary:
    Forecast start: {forecast_data['ds'].iloc[-forecast_days].date()}
    Forecast end: {forecast_data['ds'].iloc[-1].date()}
    Forecasted start price: ${round(forecast_data['yhat'].iloc[-forecast_days], 2)}
    Forecasted end price: ${round(forecast_data['yhat'].iloc[-1], 2)}
    Highest forecasted price: ${round(forecast_data['yhat'].tail(forecast_days).max(), 2)}
    Lowest forecasted price: ${round(forecast_data['yhat'].tail(forecast_days).min(), 2)}

    Please provide:
    1. A brief overview of the historical performance
    2. Key trends observed in the forecast
    3. Potential factors that might influence the stock price
    4. Any risks or opportunities for investors
    5. A concise conclusion

    Limit your response to about 150 words.
    """

    # Generate content with a couple of retries for transient errors
    last_err = None
    for _ in range(2):
        try:
            assert isinstance(model_name, str)
            return _generate_with_model(model_name, prompt)
        except google_exceptions.NotFound as e:
            # Try to re-resolve model and retry once
            st.session_state.pop("genai_working_model", None)
            model_name = _pick_supported_model()
            if model_name:
                try:
                    return _generate_with_model(model_name, prompt)
                except Exception as inner_e:
                    last_err = inner_e
                    continue
            last_err = e
        except Exception as e:
            last_err = e
    st.warning(f"AI response failed: {last_err}")
    return "AI model request failed. Please try again later."

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