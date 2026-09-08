import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

CORRECT_PASSWORD = "PowerFULLtrade"

st.set_page_config(
    page_title="Proprietary Matrix Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
if "selected_asset" not in st.session_state:
    st.session_state["selected_asset"] = "SELECT STOCK"

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
            h, l, c = float(target_df["High"]), float(target_df["Low"]), float(target_df["Close"])
            current_price = float(df["Close"].iloc[-1])
            span = h - l
            levels = {
                "Sky Target 3": l + (span * 2.0),
                "Sky Target 2": l + (span * 1.618),
                "Center Balance Zone": l + (span * 0.618),
                "Floor Support 1": l + (span * 0.272),
                "Floor Support 2": l + (span * 0.236),
                "Base Zero": l,
                "Floor Support 3": l - (span * 0.618)
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
            df = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            year_high, year_low = float(df["High"].max()), float(df["Low"].min())
            current_price = float(df["Close"].iloc[-1])
            span = year_high - year_low
            
            raw_levels = {
                "Sky Target 3": year_low + (span * 2.0),
                "Sky Target 2": year_low + (span * 1.618),
                "Sky Target 1": year_high,
                "Center Balance Zone": year_low + (span * 0.618),
                "Floor Support 1": year_low + (span * 0.272),
                "Floor Support 2": year_low + (span * 0.236),
                "Base Zero": year_low,
                "Floor Support 3": year_low - (span * 0.618),
                "Floor Support 4": year_low - (span * 1.618),
                "Floor Support 5": year_low - (span * 2.0)
            }
            
            sorted_levels = sorted(raw_levels.items(), key=lambda x: x[1])
            split_idx = 0
            for i, (name, val) in enumerate(sorted_levels):
                if current_price >= val: split_idx = i + 1
            
            start_idx = max(0, split_idx - 2)
            end_idx = min(len(sorted_levels), split_idx + 3)
            filtered_levels = dict(sorted_levels[start_idx:end_idx])
            
            prev_close = float(df["Close"].iloc[-2])
            prev_open = float(df["Open"].iloc[-2])
            prev_high = float(df["High"].iloc[-2])
            prev_low = float(df["Low"].iloc[-2])
            prev_volume = int(df["Volume"].iloc[-2])
            return {
                "Open": round(prev_open, 2), "High": round(prev_high, 2), "Low": round(prev_low, 2), "Close": round(prev_close, 2),
                "Volume": prev_volume, "Current Price": round(current_price, 2), "Calculated Levels": filtered_levels
            }
        except: return None

    st.markdown("<h1 style='text-align: center;'>🦅 Proprietary Structural Matrix Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0;'>Premium Quant Infrastructure Tool</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.subheader("🏛️ All Indices Master Track List (Daily Base Nearby Matrix)")
    with st.spinner("તમામ ઇન્ડાઇસિસ મેટ્રિક્સ લોડ થઈ રહ્યો છે..."):
        index_results = [analyze_index_daily(ticker, name) for name, ticker in all_market_indices.items() if analyze_index_daily(ticker, name) is not None]
        if len(index_results) > 0: st.dataframe(pd.DataFrame(index_results), use_container_width=True)
        else: st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")
    st.subheader("🔍 Asset Search Menu (With Auto-Suggestions)")
    
    def on_change_stock():
        selected = st.session_state.stock_selectbox
        if selected != "SELECT STOCK":
            st.session_state["active_searched"] = selected
            st.session_state.stock_selectbox = "SELECT STOCK"

    st.selectbox(
        "સ્ટોક અથવા ઇન્ડેક્સનું નામ ટાઈપ અથવા સિલેક્ટ કરો (Search with Suggestion):", 
        suggestions_pool, 
        key="stock_selectbox",
        on_change=on_change_stock
    )

    if "active_searched" in st.session_state and st.session_state["active_searched"]:
        search_query = st.session_state["active_searched"].strip().upper()
        resolved_ticker = all_market_indices[search_query] if search_query in all_market_indices else search_query + ".NS"

        with st.spinner(f"'{resolved_ticker}' નો વાર્ષિક ડેટા પ્રોસેસ થઈ રહ્યો છે..."):
            stock_res = analyze_stock_yearly(resolved_ticker)
            if stock_res:
                st.markdown(f"## 🎉 {search_query} Matrix Summary")
                col1, col2, col3 = st.columns(3)
                col1.metric("Live Market Spot", f"₹ {stock_res['Current Price']:,.2f}")
                col2.write(f"**Year Open / Close:** ₹ {stock_res['Open']} / ₹ {stock_res['Close']}")
                col3.write(f"**Accumulated Volume:** {stock_res['Volume']:,}")
                
                st.markdown("---")
                # 🔒 સુધારેલું સિક્રેટ હેડિંગ: કોઈ આંકડા કે હિન્ટ વગર પ્યોર કસ્ટમ ટેબલ
                st.markdown(f"### 🦅 Symmetrical Price Matrix")
                levels_data = [{"Easy Structural Level": name, "Calculated Price": f"₹ {val:,.2f}"} for name, val in stock_res["Calculated Levels"].items()]
                st.dataframe(pd.DataFrame(levels_data), use_container_width=True)
            else:
                st.error("❌ ડેટા મળ્યો નથી.")
    else:
