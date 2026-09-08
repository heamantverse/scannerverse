import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

st.set_page_config(
    page_title="Proprietary Matrix Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🖤 કસ્ટમ એડવાન્સ CSS - વેબસાઇટને ૧૦૦% આધુનિક અને સુંદર પ્રો લુક આપવા માટે
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
    .css-1r6slb0 { background-color: #121620; padding: 20px; border-radius: 8px; border: 1px solid #1f2430; }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏛️ ભારતના તમામ મુખ્ય ૧૦ ઇન્ડાઇસિસનું માસ્ટર મેપિંગ
all_market_indices = {
    "NIFTY 50": "^NSEI",
    "NIFTY BANK": "^NSEBANK",
    "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",
    "NIFTY MIDCAP 50": "^CRSMID",
    "NIFTY SMALLCAP 50": "^CNXSMALL",
    "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY METAL": "^CNXMETAL"
}

# 📥 ઓટો-સજેશન માટે ૨૦૦+ પાવરફુલ મોમેન્ટમ સ્ટોક્સનું લિસ્ટ
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
    "MCX", "METROPOLIS", "MFSL", "MGL", "MUTHOOTFIN", "NATIONALUM", "NAVINFLUOR", "NMDC", "OBEROIRLTY", "OFSS",
    "OIL", "PEL", "PERSISTENT", "PETRONET", "POLYCAB", "PVRINOX", "SAIL", "SUNTV", "SUPREMEIND", "SUZLON", "TATACOMM",
    "TATAELXSI", "TATACONSUM", "TECHM", "TORNTPHARM", "TORNTPOWER", "TVSMOTOR", "UBL", "UNIONBANK", "UPL", "VOLTAS", "ZEEL",
    "INFIBEAM", "HUDCO", "SJVN", "NHPC", "GMRINFRA", "IREDA", "PAYTM", "RVNL", "YESBANK", "DELHIVERY", "MANAPPURAM"
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
        
        # મુખ્ય ૧૦ લેવલ્સનું સિક્રેટ લોજિક (આંકડા વગર)
        levels = {
            "Macro Boundary High": l + (span * 2.0),
            "Primary Trajectory Axis": l + (span * 1.618),
            "Core Balance Node": l + (span * 0.618),
            "Velocity Confirmation Node": l + (span * 0.272),
            "Secondary Pivot Node": l + (span * 0.236),
            "Anchor Baseline": l,
            "Retraction Buffer Zone": l - (span * 0.618),
            "Extrapolated Range Lower": l - (span * 1.618),
            "Macro Boundary Low": l - (span * 2.0)
        }
        closest_node = "In-Between Zones"
        min_diff = float("inf")
        for name, val in levels.items():
            diff = abs(current_price - val)
            if diff < min_diff:
                min_diff = diff; closest_node = name
        return {"Index Tracker": display_name, "Current Spot": f"₹ {current_price:,.2f}", "Nearby Structural Node": f"⚡ {closest_node}"}
    except: return None

def analyze_stock_yearly(ticker_name):
    try:
        df = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
        if df.empty or len(df) < 20: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        year_high, year_low = float(df["High"].max()), float(df["Low"].min())
        current_price = float(df["Close"].iloc[-1])
        span = year_high - year_low
        
        # 🎯 પ્રો ફિલ્ટર: તમે કીધેલા જ કસ્ટમ ૧૦ લેવલ્સ (0, 0.236, 0.272, 0.618, -0.618, 1.618, -1.618, -2, 2, અને 1)
        levels = {
            "Stratosphere Extension Max [2.0]": year_low + (span * 2.0),
            "Horizon Major Axis [1.618]": year_low + (span * 1.618),
            "Yearly Ultimate High [1.0]": year_high,
            "Core Balance Node [0.618]": year_low + (span * 0.618),
            "Velocity Conformation Node [0.272]": year_low + (span * 0.272),
            "Secondary Pivot Node [0.236]": year_low + (span * 0.236),
            "Ground Zero Base [0.0]": year_low,
            "Retraction Buffer Zone [-0.618]": year_low - (span * 0.618),
            "Extrapolated Range Lower [-1.618]": year_low - (span * 1.618),
            "Macro Boundary Low [-2.0]": year_low - (span * 2.0)
        }
        prev_close = float(df["Close"].iloc[-2])
        prev_open = float(df["Open"].iloc[-2])
        prev_high = float(df["High"].iloc[-2])
        prev_low = float(df["Low"].iloc[-2])
        prev_volume = int(df["Volume"].iloc[-2])
        return {
            "Open": round(prev_open, 2), "High": round(prev_high, 2), "Low": round(prev_low, 2), "Close": round(prev_close, 2),
            "Volume": prev_volume, "Current Price": round(current_price, 2), "Calculated Levels": levels
        }
    except: return None

def run_dashboard():
    # 💎 આધુનિક હેડર સેક્શન
    st.markdown("<h1 style='text-align: center;'>🦅 Proprietary Structural Matrix Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8892b0;'>Premium Quant Infrastructure Tool</p>", unsafe_allow_html=True)
    st.markdown("---")

    # 📊 વિભાગ ૧: તમામ ઇન્ડાઇસિસનો માસ્ટર ટ્રેક લિસ્ટ (Daily Base Nearby)
    st.subheader("🏛️ All Indices Master Track List (Daily Base Nearby Matrix)")
    st.write("આ ઇન્ડાઇસિસનો ડેટા પ્યોર **Daily બેઝ** પરથી ગણવામાં આવ્યો છે અને લાઈવ રેટની **સૌથી નજીકનું લેવલ** બતાવે છે.")
    
    with st.spinner("તમામ ઇન્ડાઇસિસ મેટ્રિક્સ લોડ થઈ રહ્યો છે..."):
        index_results = [analyze_index_daily(ticker, name) for name, ticker in all_market_indices.items() if analyze_index_daily(ticker, name) is not None]
        if len(index_results) > 0:
            st.dataframe(pd.DataFrame(index_results), use_container_width=True)
        else:
            st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")
    
    # 🔍 વિભાગ ૨: ઓટો-સજેશન સર્ચ મેનુ (સુધારેલો ક્લીન લુક)
    st.subheader("🔍 Asset Search Menu (With Auto-Suggestions)")
    st.write("નીચે બોક્સ પર ક્લિક કરીને નામ ટાઈપ કરો, આખા લિસ્ટમાંથી **ઓટો-સજેશન** આવી જશે. સિલેક્ટ કરતા જ તેનો **Yearly હોલ ડેટા** દેખાશે.")
    
    user_choice = st.selectbox("સ્ટોક અથવા ઇન્ડેક્સનું નામ ટાઈપ અથવા સિલેક્ટ કરો (Search with Suggestion):", suggestions_pool, index=0)

    if user_choice and user_choice != "SELECT STOCK":
        search_query = user_choice.strip().upper()
        resolved_ticker = all_market_indices[search_query] if search_query in all_market_indices else search_query + ".NS"

        with st.spinner(f"'{resolved_ticker}' નો વાર્ષિક (Yearly) સંપૂર્ણ ડેટા પ્રોસેસ થઈ રહ્યો છે..."):
            stock_res = analyze_stock_yearly(resolved_ticker)
            if stock_res:
                st.markdown(f"## 🎉 {search_query} Matrix Summary")
                
                # કલરફુલ પ્રીમિયમ કાર્ડ ડિઝાઇન (Candle Stats)
                col1, col2, col3 = st.columns(3)
                col1.metric("Live Market Spot", f"₹ {stock_res['Current Price']:,.2f}")
                col2.write(f"**Year Open / Close:** ₹ {stock_res['Open']} / ₹ {stock_res['Close']}")
                col3.write(f"**Accumulated Volume:** {stock_res['Volume']:,}")
                
                c_a, c_b = st.columns(2)
                c_a.write(f"🟢 **Year High Bound:** ₹ {stock_res['High']}")
                c_b.write(f"🔴 **Year Low Bound:** ₹ {stock_res['Low']}")
                
                st.markdown("---")
                # 🎯 શુદ્ધ ૧૦ સિક્રેટ લેવલ્સ વાળું નવું ક્લીન ટેબલ
                st.markdown(f"### 🦅 Complete Symmetrical Matrix (1-Year Levels)")
                
                levels_data = [{"Matrix Structural Node": name, "Calculated Threshold": f"₹ {val:,.2f}"} for name, val in stock_res["Calculated Levels"].items()]
                st.dataframe(pd.DataFrame(levels_data), use_container_width=True)
            else:
                st.error("❌ આ સ્ટોક માટે કોઈ ડેટા મળ્યો નથી.")
    else:
        st.info("💡 ઉપર સર્ચ મેનુમાંથી કોઈ એક સ્ટોક કે ઇન્ડેક્સ પસંદ કરો, અત્યારે નીચે કોઈ ડેટા લોડ કરેલો નથી.")

    st.markdown("---")
