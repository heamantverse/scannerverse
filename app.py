import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

# 🤖 🛠️ ટેલિગ્રામ કનેક્શન સેટઅપ (મેં તમારો આઈડી અને ટોકન અહીં કસ્ટમ ફોર્મેટમાં સેટ કરી દીધા છે)
TELEGRAM_TOKEN = "8879164929:AAHo9RfH2hBpSW062hP0J1aMbx9xMdAJ90g"
TELEGRAM_CHAT_ID = "381187243"

# ટેલિગ્રામ પર ઓટોમેટિક ફ્રી મેસેજ મોકલવાનું સ્માર્ટ ફંક્શન
def send_telegram_alert(message_text):
    if TELEGRAM_TOKEN and TELEGRAM_TOKEN != "":
        try:
            url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message_text, "parse_mode": "Markdown"}
            res = requests.post(url, json=payload, timeout=5)
            return res.status_code == 200
        except:
            return False
    return False

st.set_page_config(
    page_title="Proprietary Matrix Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# કસ્ટમ CSS ડાર્ક થીમ
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0e14; color: #ecf0f1; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #00ffaa !important; font-weight: 700; }
    .stButton>button { background: linear-gradient(135deg, #00ffaa 0%, #00bcff 100%); color: #0b0e14 !important; font-weight: bold; border: none; padding: 10px 24px; border-radius: 6px; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,255,170,0.4); }
    .stTextInput>div>div>input { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; border-radius: 6px; }
    .stSelectbox>div>div>div { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; border-radius: 6px; }
    div[data-testid="stMetricValue"] { color: #00ffaa !important; font-size: 32px; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "final_search_query" not in st.session_state:
    st.session_state["final_search_query"] = None

all_market_indices = {
    "NIFTY 50": "^NSEI", "NIFTY BANK": "^NSEBANK", "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",
    "NIFTY MIDCAP 50": "^CRSMID", "NIFTY SMALLCAP 50": "^CNXSMALL", "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO", "NIFTY PHARMA": "^CNXPHARMA", "NIFTY FMCG": "^CNXFMCG", "NIFTY METAL": "^CNXMETAL"
}

suggestions_pool = [
    "SELECT STOCK", "NIFTY 50", "NIFTY BANK", "NIFTY FINANCIAL SERVICES", "NIFTY IT", "NIFTY AUTO", "NIFTY PHARMA", "NIFTY FMCG", "NIFTY METAL",
    "RELIANCE", "TCS", "INFY", "SBIN", "HDFCBANK", "ICICIBANK", "TATAMOTORS", "BHARTIARTL", "ITC", "HINDUNILVR",
    "LT", "BAJFINANCE", "MARUTI", "HCLTECH", "AXISBANK", "SUNPHARMA", "M&M", "TATASTEEL", "ADANIENT", "NTPC",
    "POWERGRID", "TITAN", "ULTRACEMCO", "COALINDIA", "BAJAJFINSV", "ONGC", "ADANIPORTS", "HINDALCO", "JSWSTEEL", "WIPRO",
    "NESTLEIND", "DRREDDY", "APOLLOHOSP", "SBILIFE", "BRITANNIA", "SHRIRAMFIN", "BAJAJ-AUTO", "BEL", "EICHERMOT", "HEROMOTOCO",
    "CIPLA", "DIVISLAB", "INDUSINDBK", "KOTAKBANK", "PNB", "BANKBARODA", "FEDERALBNK", "IDFCFIRSTB", "BANDHANBNK", "HAL",
    "ZOMATO", "TRENT", "VBL", "DLF", "IRFC", "RECLTD", "PFC", "IOC", "GAIL", "TATAPOWER", "CANBK", "CHOLAFIN",
    "JINDALSTEL", "AMBUJACEM", "HAVELLS", "PIDILITIND", "ADANIPOWER", "BHEL", "AUROPHARMA", "BANKINDIA", "BOSCHLTD", "DABUR",
    "DEEPAKNTR", "EXIDEIND", "GLENMARK", "GODREJPROP", "GRANULES", "GUJGASLTD", "INDIGO", "IRCTC", "JSWENERGY", "JUBLFOOD",
    "MCX", "METROPOLIS", "MFSL", "MGL", "MUTHOOTFIN", "NATIONALUM", "NAVINFLUOR", "NMDC", "NYKAA", "OBEROIRLTY", "OFSS",
    "OIL", "PAYTM", "PEL", "PERSISTENT", "PETRONET", "POLYCAB", "PVRINOX", "RAMCOCEM", "RVNL", "SAIL", "SOBHA", "SONACOMS", "SUNTV", "SUPREMEIND", "SUZLON", "TATACOMM",
    "TATAELXSI", "TATACONSUM", "TECHM", "TORNTPHARM", "TORNTPOWER", "TVSMOTOR", "UBL", "UNIONBANK", "UPL", "VOLTAS", "ZEEL",
    "INFIBEAM", "HUDCO", "SJVN", "NHPC", "GMRINFRA", "IREDA", "YESBANK", "DELHIVERY", "MANAPPURAM"
]

def analyze_index_daily(ticker_name, display_name):
    try:
        df = yf.download(ticker_name, period="5d", auto_adjust=True, progress=False)
        if df.empty or len(df) < 2: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        target_df = df.iloc[-2]
        h, l = float(target_df["High"]), float(target_df["Low"])
        current_price = float(df["Close"].iloc[-1])
        span = h - l
        levels = {
            "Sky Target 3": l + (span * 2.0), "Sky Target 2": l + (span * 1.618), "Center Balance Zone": l + (span * 0.618),
            "Floor Support 1": l + (span * 0.272), "Floor Support 2": l + (span * 0.236), "Base Zero": l, "Floor Support 3": l - (span * 0.618)
        }
        closest_node = "In-Between Zones"
        min_diff = float("inf")
        for name, val in levels.items():
            diff = abs(current_price - val)
            if diff < min_diff: min_diff = diff; closest_node = name
        return {"Index Tracker": display_name, "Current Spot": f"₹ {current_price:,.2f}", "Nearby Node Level": f"⚡ {closest_node}"}
    except: return None

def analyze_stock_yearly(ticker_name):
    try:
        df_hist = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
        if df_hist.empty or len(df_hist) < 20: return None
        if isinstance(df_hist.columns, pd.MultiIndex): df_hist.columns = df_hist.columns.get_level_values(0)
        year_high, year_low = float(df_hist["High"].max()), float(df_hist["Low"].min())
        span = year_high - year_low
        
        df_today = yf.download(ticker_name, period="2d", auto_adjust=True, progress=False)
        if isinstance(df_today.columns, pd.MultiIndex): df_today.columns = df_today.columns.get_level_values(0)
        
        current_price = float(df_today["Close"].iloc[-1])
        today_open = float(df_today["Open"].iloc[-1])
        today_high = float(df_today["High"].iloc[-1])
        today_low = float(df_today["Low"].iloc[-1])
        prev_close = float(df_today["Close"].iloc[-2])
        today_volume = int(df_today["Volume"].iloc[-1])
        
        raw_levels = {
            "Sky Target 3": year_low + (span * 2.0), "Sky Target 2": year_low + (span * 1.618), "Sky Target 1": year_high,
            "Center Balance Zone": year_low + (span * 0.618), "Floor Support 1": year_low + (span * 0.272), "Floor Support 2": year_low + (span * 0.236),
            "Base Zero": year_low, "Floor Support 3": year_low - (span * 0.618), "Floor Support 4": year_low - (span * 1.618), "Macro Boundary Low": year_low - (span * 2.0)
        }
        
        sorted_levels = sorted(raw_levels.items(), key=lambda x: x[1])
        split_idx = 0
        for i, (name, val) in enumerate(sorted_levels):
            if current_price >= val: split_idx = i + 1
                
        start_idx = max(0, split_idx - 2)
        end_idx = min(len(sorted_levels), split_idx + 3)
        filtered_levels = dict(sorted_levels[start_idx:end_idx])
        
        return {
            "Today Open": round(today_open, 2), "Today High": round(today_high, 2), "Today Low": round(today_low, 2),
            "Prev Close": round(prev_close, 2), "Volume": today_volume, "Current Price": round(current_price, 2), "Calculated Levels": filtered_levels
        }
    except: return None

# --- મેઈન ગેઇટવે કંટ્રોલ ફ્લો ---
if st.session_state["authenticated"] == False:
    st.markdown("<h1>🔒 Security Access Required</h1>", unsafe_allow_html=True)
    st.write("આ એક પ્રાઇવેટ પ્રોપ્રાઇટરી મેટ્રિક્સ સ્કેનર છે.")
    user_password = st.text_input("Enter Private Access Password:", type="password")
    if st.button("Access Dashboard"):
        if user_password == CORRECT_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ ખોટો પાસવર્ડ!")
else:
    st.markdown("<h1 style='text-align: center;'>🦅 Proprietary Structural Matrix Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0;'>Premium Quant Infrastructure Tool</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.sidebar.subheader("🤖 Connection Diagnostics")
    if st.sidebar.button("⚡ Test Telegram Alert"):
        success = send_telegram_alert("🚀 *SUCCESS:* Your Scanner is now successfully linked to this Telegram Profile!")
        if success: st.sidebar.success("✅ મેસેજ મોકલાઈ ગયો! ટેલિગ્રામ ચેક કરો.")
        else: st.sidebar.error("❌ મેસેજ ન ગયો. પ્લીઝ બોટ પર જઈને Start દબાવો.")

    # ૧. ઇન્ડાઇસિસ માસ્ટર ટ્રેક લિસ્ટ
    st.subheader("🏛️ All Indices Master Track List (Daily Base Nearby Matrix)")
    index_results = [analyze_index_daily(ticker, name) for name, ticker in all_market_indices.items() if analyze_index_daily(ticker, name) is not None]
    if len(index_results) > 0:
        st.dataframe(pd.DataFrame(index_results), use_container_width=True)
    else:
        st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")
    st.subheader("🔍 Asset Search Menu (With Suggestions)")

    def handle_selectbox_change():
        selected = st.session_state.stock_selectbox_key
        if selected != "SELECT STOCK":
            st.session_state["final_search_query"] = selected

    st.selectbox(
        "સ્ટોક અથવા ઇન્ડેક્સનું નામ સિલેક્ટ કરો (સજેશન જોવા માટે અક્ષર ટાઈપ કરો):",
        suggestions_pool,
        key="stock_selectbox_key",
        index=0,
        on_change=handle_selectbox_change
    )

    search_query_active = st.session_state["final_search_query"]

    if search_query_active:
        search_query = search_query_active.strip().upper()
        resolved_ticker = all_market_indices[search_query] if search_query in all_market_indices else search_query + ".NS"

        # 🛠️ એરર ફિક્સ: ડેટા રીડિંગ મિકેનિઝમ સુધારી દીધું જેથી ક્યારેય ડેટા અદ્રશ્ય ન થાય
