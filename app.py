import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ અને આઈડી
CORRECT_USER_ID = "SupaTrade"
CORRECT_PASSWORD = "PowerFULLtrade"

st.set_page_config(
    page_title="SUPA TRADE R - Matrix Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# કસ્ટમ CSS થીમ - સ્કેચ મુજબ પ્રીમિયમ લુક આપવા માટે
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0e14; color: #ecf0f1; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #00ffaa !important; font-weight: 700; text-align: center; }
    .stButton>button { background: linear-gradient(135deg, #00ffaa 0%, #00bcff 100%); color: #0b0e14 !important; font-weight: bold; border: none; padding: 12px 28px; border-radius: 6px; width: 100%; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(0,255,170,0.4); }
    .stTextInput>div>div>input { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; border-radius: 6px; }
    .stSelectbox>div>div>div { background-color: #161b22; color: #ffffff; border: 1px solid #30363d; border-radius: 6px; }
    .custom-card { background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2430; margin-top: 15px; }
    .level-line { padding: 10px 0; border-bottom: 1px solid #1f2430; font-size: 16px; }
    .ma-line { padding: 10px; background-color: #161b22; border-radius: 6px; border: 1px solid #30363d; margin-bottom: 10px; font-size: 16px; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- ૧. લૉગિન પેજ ---
if not st.session_state["authenticated"]:
    st.markdown("<h1 style='font-size: 42px; font-style: italic; letter-spacing: 2px;'>⚡ SUPA TRADE R ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0;'>Private Quantitative Trading Software</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<h3 style='text-align: left; color: #ffffff !important;'>LOGIN DETAILS</h3>", unsafe_allow_html=True)
        user_id = st.text_input("Enter Private User ID:", placeholder="e.g., SupaTrade")
        user_password = st.text_input("Enter Private Access Password:", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Access Dashboard"):
            if user_id == CORRECT_USER_ID and user_password == CORRECT_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else: st.error("❌ ખોટો યુઝર આઈડી અથવા પાસવર્ડ!")
                
    st.markdown("<br><br><hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #ff4b4b !important; text-align: center;'>Disclaimer</h4>", unsafe_allow_html=True)
    st.caption("<p style='text-align: center;'>This is a private proprietary system. Unauthorized access attempts are strictly monitored and logged.</p>", unsafe_allow_html=True)

else:
    # --- ૨. મુખ્ય ડેશબોર્ડ ---
    st.markdown("<h1>🦅 CREATE THE BEST OPPORTUNITY </h1>", unsafe_allow_html=True)
    st.markdown("---")

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
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            df.columns = [str(c).strip() for c in df.columns]
        return df

    def extract_scalar(series_or_val):
        if isinstance(series_or_val, (pd.Series, np.ndarray)):
            return float(series_or_val.iloc[0]) if len(series_or_val) > 0 else 0.0
        return float(series_or_val)

    def analyze_full_matrix(ticker_name):
        try:
            df_hist = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
            if df_hist.empty: return None
            df_hist = clean_columns(df_hist)
            
            ma_50 = float(df_hist["Close"].rolling(50).mean().dropna().iloc[-1])
            ma_100 = float(df_hist["Close"].rolling(100).mean().dropna().iloc[-1])
            ma_200 = float(df_hist["Close"].rolling(200).mean().dropna().iloc[-1])
            
            year_high = float(df_hist["High"].max())
            year_low = float(df_hist["Low"].min())
            span = year_high - year_low
            
            df_today = yf.download(ticker_name, period="2d", auto_adjust=True, progress=False)
            if df_today.empty: return None
            df_today = clean_columns(df_today)
            
            t_row = df_today.iloc[-1]
            current_price = extract_scalar(t_row["Close"])
            today_open = extract_scalar(t_row["Open"])
            today_high = extract_scalar(t_row["High"])
            today_low = extract_scalar(t_row["Low"])
            avg_vol = int(df_hist["Volume"].mean())
            
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
                "Open": today_open, "High": today_high, "Low": today_low, "Close": current_price,
                "Avg Vol": avg_vol, "MA50": ma_50, "MA100": ma_100, "MA200": ma_200,
                "Current Price": current_price, "Calculated Levels": filtered_levels
            }
        except: return None

    st.markdown("<h3 style='text-align: center; color: #00ffaa;'>... [ SEARCH ] ...</h3>", unsafe_allow_html=True)
    user_choice = st.selectbox("", suggestions_pool, index=0, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    if user_choice and user_choice != "SELECT STOCK":
        search_query = user_choice.strip().upper()
        resolved_ticker = all_market_indices[search_query] if search_query in all_market_indices else search_query + ".NS"

        with st.spinner("લાયવ ક્વોન્ટ ડેટા કેલ્ક્યુલેટ થઈ રહ્યો છે..."):
            res = analyze_full_matrix(resolved_ticker)
            
            if res:
                st.markdown("### - . RESULT . -")
                
                hloc_data = {
                    "SCRIP": [search_query],
                    "TODAYS H": [f"₹ {res['High']:,.2f}"],
                    "TODAYS L": [f"₹ {res['Low']:,.2f}"],
                    "TODAYS O": [f"₹ {res['Open']:,.2f}"],
                    "TODAYS C": [f"₹ {res['Close']:,.2f}"],
                    "Avg Vol": [f"{res['Avg Vol']:,}"]
                }
                st.markdown("**TODAYS MARKET FEED & VOLUME**")
                st.dataframe(pd.DataFrame(hloc_data), use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown("### 📊 QUANT SYMMETRICAL MATRIX & MOVING AVERAGES ANALYSIS")
                
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
