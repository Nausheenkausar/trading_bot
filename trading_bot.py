import streamlit as st
from binance.client import Client
from binance.enums import *
import logging

# Setup logging
logging.basicConfig(filename='trading_bot_ui.log', level=logging.INFO)

# Get credentials from Streamlit secrets
API_KEY = st.secrets["binance"]["api_key"]
API_SECRET = st.secrets["binance"]["api_secret"]

# Connect to Binance Futures Testnet
client = Client(API_KEY, API_SECRET)
client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

st.set_page_config(page_title="Binance Futures Bot", layout="centered")
st.title("🟢 Binance Futures Trading Bot (Testnet)")

# User input
symbol = st.text_input("Enter Symbol (e.g., BTCUSDT)", "BTCUSDT")
side = st.selectbox("Side", ["BUY", "SELL"])
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_MARKET"])
quantity = st.number_input("Quantity", min_value=0.001, value=0.001, step=0.001)

# Additional fields based on order type
price = stop_price = None
if order_type == "LIMIT":
    price = st.number_input("Limit Price", min_value=0.0, value=30000.0, step=10.0)
elif order_type == "STOP_MARKET":
    stop_price = st.number_input("Stop Price", min_value=0.0, value=29500.0, step=10.0)

# Place order
if st.button("Place Order"):
    try:
        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=ORDER_TYPE_MARKET,
                quantity=quantity
            )

        elif order_type == "LIMIT":
            order = client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price
            )

        elif order_type == "STOP_MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=SIDE_BUY if side == "BUY" else SIDE_SELL,
                type=ORDER_TYPE_STOP_MARKET,
                stopPrice=stop_price,
                quantity=quantity,
                timeInForce=TIME_IN_FORCE_GTC
            )

        st.success("✅ Order Placed Successfully!")
        st.json(order)
        logging.info(f"Order placed: {order}")

    except Exception as e:
        st.error(f"❌ Error placing order: {e}")
        logging.error(f"Order error: {e}")
