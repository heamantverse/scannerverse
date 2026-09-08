import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

# 🤖 🛠️ ટેલિગ્રામ કનેક્શન સેટઅપ
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

def clean_columns(df):
    if df is not None and not df.empty:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df.columns = [str(c).strip() for c in df.columns]
    return df

def analyze_index_daily(ticker_name, display_name):
    try:
        df = yf.download(ticker_name, period="5d", auto_adjust=True, progress=False)
        if df.empty or len(df) < 2: return None
        df = clean_columns(df)
        
        target_df = df.iloc[-2]
        h = float(target_df["High"].iloc if isinstance(target_df["High"], pd.Series) else target_df["High"])
        l = float(target_df["Low"].iloc if isinstance(target_df["Low"], pd.Series) else target_df["Low"])
        
        last_row = df.iloc[-1]
        current_price = float(last_row["Close"].iloc if isinstance(last_row["Close"], pd.Series) else last_row["Close"])
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
        df_hist = clean_columns(df_hist)
        
        year_high = float(df_hist["High"].max().iloc if isinstance(df_hist["High"].max(), pd.Series) else df_hist["High"].max())
        year_low = float(df_hist["Low"].min().iloc if isinstance(df_hist["Low"].min(), pd.Series) else df_hist["Low"].min())
        span = year_high - year_low
        
        df_today = yf.download(ticker_name, period="2d", auto_adjust=True, progress=False)
        if df_today.empty or len(df_today) < 2: return None
        df_today = clean_columns(df_today)
        
        t_row = df_today.iloc[-1]
        p_row = df_today.iloc[-2]
        
        current_price = float(t_row["Close"].iloc if isinstance(t_row["Close"], pd.Series) else t_row["Close"])
        today_open = float(t_row["Open"].iloc if isinstance(t_row["Open"], pd.Series) else t_row["Open"])
        today_high = float(t_row["High"].iloc if isinstance(t_row["High"], pd.Series) else t_row["High"])
        today_low = float(t_row["Low"].iloc if isinstance(t_row["Low"], pd.Series) else t_row["Low"])
        prev_close = float(p_row["Close"].iloc if isinstance(p_row["Close"], pd.Series) else p_row["Close"])
        today_volume = int(t_row["Volume"].iloc if isinstance(t_row["Volume"], pd.Series) else t_row["Volume"])
        
        raw_levels = {
            "Sky Target 3": year_low + (span * 2.0), "Sky Target 2": year_low + (span * 1.618), "Sky Target 1": year_high,
            "Center Balance Zone": year_low + (span * 0.618), "Floor Support 1": year_low + (span * 0.272), "Floor Support 2": year_low + (span * 0.236),
            "Base Zero": year_low, "Floor Support 3": year_low - (span * 0.618), "Floor Support 4": year_low - (span * 1.618), "Macro Boundary Low": year_low - (span * 2.0)
        }
        
        sorted_levels = sorted(raw_levels.items(), key=lambda x: x)
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

# --- મુખ્ય ગેઇટવે કંટ્રોલ ફ્લો ---
if not st.session_state["authenticated"]:
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
        success = send_telegram_alert("🚀 *SUCCESS:* Your Scanner is now linked successfully to your Telegram Profile ID!")
        if success: st.sidebar.success("✅ મેસેજ મોકલાઈ ગયો!")
        else: st.sidebar.error("❌ બોટ સ્ટાર્ટ કરો.")

    st.subheader("🏛️ All Indices Master Track List (Daily Base Nearby Matrix)")
    
    # 🛠️ સચોટ ફિક્સ: અધૂરો લૂપ કૌંસ અહીં સંપૂર્ણ સાચો સેટ કરી દીધો છે
    index_results = []
    for name, ticker in all_market_indices.items():
        res = analyze_index_daily(ticker, name)
        if res is not None:
            index_results.append(res)
            
    if len(index_results) > 0:
        st.dataframe(pd.DataFrame(index_results), use_container_width=True)
    else:
        st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")
    st.subheader("🔍 Asset Search Menu")

    user_choice = st.selectbox(
