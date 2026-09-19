import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Real-Time Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("📈 Real-Time Stock Market Dashboard")

st.markdown(
    "Track and visualize live/intraday stock market data "
    "with interactive charts and financial indicators."
)

# ==========================================================
# API CONFIGURATION
# ==========================================================

API_KEY = st.sidebar.text_input(
    "🔑 Enter Twelve Data API Key",
    type="password"
).strip()

# ==========================================================
# STOCK LIST
# ==========================================================

stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Google": "GOOGL",
    "Amazon": "AMZN",
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Meta": "META",
    "Netflix": "NFLX",
    "Intel": "INTC",
    "AMD": "AMD"
}

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("⚙️ Dashboard Settings")

selected_company = st.sidebar.selectbox(
    "Select Stock",
    list(stocks.keys())
)

symbol = stocks[selected_company]

# ==========================================================
# TIME INTERVAL
# ==========================================================

interval = st.sidebar.selectbox(
    "Select Time Interval",
    [
        "1min",
        "5min",
        "15min",
        "30min",
        "1h"
    ]
)

# ==========================================================
# NUMBER OF DATA POINTS
# ==========================================================

output_size = st.sidebar.selectbox(
    "Number of Data Points",
    [50, 100, 200, 500],
    index=1
)

# ==========================================================
# AUTO REFRESH
# ==========================================================

auto_refresh = st.sidebar.checkbox(
    "🔄 Auto Refresh",
    value=False
)

refresh_seconds = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=15,
    max_value=300,
    value=30,
    step=15
)

# ==========================================================
# MANUAL REFRESH
# ==========================================================

refresh_button = st.sidebar.button(
    "🔄 Refresh Stock Data"
)

# ==========================================================
# FUNCTION: GET STOCK DATA
# ==========================================================

def get_stock_data(
    symbol,
    interval,
    api_key,
    output_size
):

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": output_size,
        "apikey": api_key
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        # --------------------------------------------------
        # API ERROR
        # --------------------------------------------------

        if data.get("status") == "error":

            error_message = data.get(
                "message",
                "Unknown API error"
            )

            st.error(
                f"❌ API Error: {error_message}"
            )

            return None

        # --------------------------------------------------
        # CHECK VALUES
        # --------------------------------------------------

        if "values" not in data:

            st.error(
                "❌ No stock data was returned by the API."
            )

            return None

        # --------------------------------------------------
        # CREATE DATAFRAME
        # --------------------------------------------------

        df = pd.DataFrame(
            data["values"]
        )

        # --------------------------------------------------
        # CONVERT DATETIME
        # --------------------------------------------------

        df["datetime"] = pd.to_datetime(
            df["datetime"]
        )

        # --------------------------------------------------
        # SORT DATA
        # --------------------------------------------------

        df = df.sort_values(
            "datetime"
        )

        # --------------------------------------------------
        # NUMERIC COLUMNS
        # --------------------------------------------------

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        # --------------------------------------------------
        # REMOVE MISSING VALUES
        # --------------------------------------------------

        df = df.dropna(
            subset=[
                "open",
                "high",
                "low",
                "close"
            ]
        )

        return df

    # ------------------------------------------------------
    # REQUEST ERROR
    # ------------------------------------------------------

    except requests.exceptions.RequestException as e:

        st.error(
            f"❌ Network error: {e}"
        )

        return None

    # ------------------------------------------------------
    # GENERAL ERROR
    # ------------------------------------------------------

    except Exception as e:

        st.error(
            f"❌ Error fetching stock data: {e}"
        )

        return None


# ==========================================================
# API KEY CHECK
# ==========================================================

if not API_KEY:

    st.info(
        "👈 Enter your Twelve Data API key "
        "in the sidebar to start."
    )

    st.markdown(
        """
        ### 🚀 How to use this dashboard

        1. Enter your Twelve Data API key.
        2. Select a stock.
        3. Select a time interval.
        4. Select the number of data points.
        5. Click **Refresh Stock Data**.
        6. View the price, charts, volume and stock table.
        """
    )

    st.stop()


# ==========================================================
# FETCH DATA
# ==========================================================

with st.spinner(
    f"Fetching {selected_company} ({symbol}) data..."
):

    df = get_stock_data(
        symbol,
        interval,
        API_KEY,
        output_size
    )

# ==========================================================
# CHECK DATA
# ==========================================================

if df is None or df.empty:

    st.error(
        "Unable to retrieve stock data. "
        "Please check your API key, symbol or API limit."
    )

    st.stop()


# ==========================================================
# LATEST DATA
# ==========================================================

latest = df.iloc[-1]

current_price = float(
    latest["close"]
)

current_open = float(
    latest["open"]
)

current_high = float(
    latest["high"]
)

current_low = float(
    latest["low"]
)

current_volume = float(
    latest.get("volume", 0)
)


# ==========================================================
# PREVIOUS DATA
# ==========================================================

if len(df) >= 2:

    previous_price = float(
        df.iloc[-2]["close"]
    )

else:

    previous_price = current_price


price_change = (
    current_price - previous_price
)

percentage_change = (
    price_change / previous_price * 100
    if previous_price != 0
    else 0
)


# ==========================================================
# DASHBOARD METRICS
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Current Price",
    f"${current_price:.2f}",
    f"{price_change:+.2f}"
)

col2.metric(
    "📊 Change %",
    f"{percentage_change:+.2f}%"
)

col3.metric(
    "🔼 Latest High",
    f"${current_high:.2f}"
)

col4.metric(
    "🔽 Latest Low",
    f"${current_low:.2f}"
)


st.divider()


# ==========================================================
# STOCK INFORMATION
# ==========================================================

st.subheader(
    f"📊 {selected_company} ({symbol})"
)

info1, info2, info3 = st.columns(3)

info1.write(
    f"**Interval:** {interval}"
)

info2.write(
    f"**Last Data Point:** "
    f"{df['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')}"
)

info3.write(
    f"**Dashboard Updated:** "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
)


# ==========================================================
# PRICE INFORMATION
# ==========================================================

st.subheader("💹 Financial Indicators")

indicator1, indicator2, indicator3, indicator4 = st.columns(4)

indicator1.metric(
    "Open",
    f"${current_open:.2f}"
)

indicator2.metric(
    "High",
    f"${current_high:.2f}"
)

indicator3.metric(
    "Low",
    f"${current_low:.2f}"
)

indicator4.metric(
    "Volume",
    f"{current_volume:,.0f}"
)


# ==========================================================
# LINE CHART
# ==========================================================

st.subheader("📈 Price Chart")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["datetime"],
        y=df["close"],
        mode="lines",
        name="Close Price",
        line=dict(
            width=2
        )
    )
)

fig.update_layout(
    title=f"{symbol} {interval} Price",
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    hovermode="x unified",
    height=500
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ==========================================================
# CANDLESTICK CHART
# ==========================================================

st.subheader("🕯️ Candlestick Chart")

candle = go.Figure()

candle.add_trace(
    go.Candlestick(
        x=df["datetime"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name=symbol
    )
)

candle.update_layout(
    title=f"{symbol} Candlestick Chart",
    xaxis_title="Time",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
    height=600
)

st.plotly_chart(
    candle,
    width="stretch"
)


# ==========================================================
# VOLUME CHART
# ==========================================================

st.subheader("📊 Trading Volume")

volume_fig = go.Figure()

volume_fig.add_trace(
    go.Bar(
        x=df["datetime"],
        y=df["volume"],
        name="Volume"
    )
)

volume_fig.update_layout(
    title=f"{symbol} Trading Volume",
    xaxis_title="Time",
    yaxis_title="Volume",
    height=400
)

st.plotly_chart(
    volume_fig,
    width="stretch"
)


# ==========================================================
# DATA TABLE
# ==========================================================

st.subheader("📋 Stock Data")

display_df = df.copy()

display_df = display_df.sort_values(
    "datetime",
    ascending=False
)

display_df["open"] = display_df["open"].round(2)
display_df["high"] = display_df["high"].round(2)
display_df["low"] = display_df["low"].round(2)
display_df["close"] = display_df["close"].round(2)

if "volume" in display_df.columns:

    display_df["volume"] = (
        display_df["volume"]
        .fillna(0)
        .astype(int)
    )

st.dataframe(
    display_df,
    width="stretch"
)


# ==========================================================
# DOWNLOAD CSV
# ==========================================================

st.subheader("📥 Download Data")

csv_data = display_df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Stock Data CSV",
    data=csv_data,
    file_name=(
        f"{symbol}_{interval}_stock_data.csv"
    ),
    mime="text/csv"
)


# ==========================================================
# REFRESH INFORMATION
# ==========================================================

if auto_refresh:

    st.sidebar.success(
        f"Auto refresh enabled: "
        f"every {refresh_seconds} seconds."
    )

else:

    st.sidebar.info(
        "Auto refresh is disabled. "
        "Use Refresh Stock Data manually."
    )







