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

# કસ્ટમ CSS ડાર્ક થીમ
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #262730; color: white; border-radius: 5px; }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    .stSelectbox>div>div>div { background-color: #262730; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if not st.session_state["authenticated"]:
        st.title("🔒 Security Access Required")
        st.write("આ એક પ્રાઇવેટ પ્રોપ્રાઇટરી મેટ્રિક્સ સ્કેનર છે.")
        user_password = st.text_input("Enter Private Access Password:", type="password")
        if st.button("Access Dashboard"):
            if user_password == CORRECT_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ ખોટો પાસવર્ડ! એક્સેસ નકારવામાં આવ્યો છે.")
        return False
    return True

if check_password():
    # 🏛️ ભારતના તમામ નાના-મોટા સેક્ટર અને ઇન્ડાઇસિસનું માસ્ટર મેપિંગ
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

    # 📥 ઓટો-સજેશન માટે ઇન-બિલ્ટ ૨૦૦+ સ્ટોક્સનું આખું લિસ્ટ (સાદા નામો સાથે)
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

    # ⏳ લોજિક ૧: ઇન્ડૅક્સ માટે પ્યોર DAILY બેઝ એનાલિસિસ ફંક્શન
    def analyze_index_daily(ticker_name, display_name):
        try:
            df = yf.download(ticker_name, period="5d", auto_adjust=True, progress=False)
            if df.empty or len(df) < 2: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
            target_df = df.iloc[-2]
            h, l, c = float(target_df["High"]), float(target_df["Low"]), float(target_df["Close"])
            current_price = float(df["Close"].iloc[-1])
            span = h - l
            
            # 🔒 ફિબોનાચી આંકડા વગરનું પ્યોર સિક્રેટ લોજિક
            levels = {
                "Stratosphere Zone": l + (span * 4.236),
                "Horizon Axis": l + (span * 1.618),
                "Core Balance Node": l + (span * 0.618),
                "Ground Zero": l
            }
            
            closest_node = "In-Between Zones"
            min_diff = float("inf")
            for name, val in levels.items():
                diff = abs(current_price - val)
                if diff < min_diff:
                    min_diff = diff; closest_node = name
            
            return {
                "Index Tracker": display_name,
                "Current Spot": round(current_price, 2),
                "Nearby Structural Node": closest_node
            }
        except: return None

    # 📈 લોજિક ૨: સ્ટોક્સ માટે પ્યોર YEARLY બેઝ એનાલિસિસ ફંક્શન (સંપૂર્ણ ડેટા માટે)
    def analyze_stock_yearly(ticker_name):
        try:
            df = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
            year_high, year_low = float(df["High"].max()), float(df["Low"].min())
            current_price = float(df["Close"].iloc[-1])
            span = year_high - year_low
            
            # 🔒 ૧૦０% સુરક્ષિત: ક્યાંય કોઈ ફિબોનાચી આંકડો કે હિન્ટ બતાવવામાં આવી નથી
            levels = {
                "Stratosphere Matrix Max": year_low + (span * 4.236),
                "Stratosphere Boundary": year_low + (span * 3.414),
                "Stratosphere Core": year_low + (span * 2.618),
                "Upper Conformation Threshold": year_low + (span * 2.0),
                "Horizon Axis": year_low + (span * 1.618),
                "Velocity Intermission Zone": year_low + (span * 1.272),
                "Core Balance Node": year_low + (span * 0.618),
                "Secondary Pivot Node": year_low + (span * 0.236),
                "Ground Zero Base": year_low,
                "Retraction Buffer Zone": year_low - (span * 0.618),
                "Extrapolated Range Lower": year_low - (span * 1.618),
                "Lower Conformation Threshold": year_low - (span * 2.0),
                "Structural Variance Low": year_low - (span * 2.618),
                "Lower Multiplier Extension": year_low - (span * 3.414),
                "Macro Boundary Low": year_low - (span * 4.236),
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

    # --- મેઈન ડેશબોર્ડ લેઆઉટ ---
    st.title("🦅 Proprietary Structural Matrix Scanner (PRO)")
    st.markdown("---")

    # 📊 વિભાગ ૧: માસ્ટર ટ્રેક લિસ્ટ (ભારતના તમામ મુખ્ય ઇન્ડાઇસિસ ડેઇલી Nearby બેઝ)
    st.subheader("🏛️ All Indices Master Track List (Daily Base Nearby Matrix)")
    st.write("ભારતના તમામ મુખ્ય ઇન્ડાઇસિસનો ડેટા પ્યોર **Daily બેઝ** પરથી ગણવામાં આવ્યો છે અને લાઈવ રેટની **સૌથી નજીકનું લેવલ** બતાવે છે.")
    
    with st.spinner("તમામ ઇન્ડાઇસિસ મેટ્રિક્સ લોડ થઈ રહ્યો છે..."):
        index_results = []
        for name, ticker in all_market_indices.items():
            res = analyze_index_daily(ticker, name)
            if res: index_results.append(res)
        
        if len(index_results) > 0:
            st.dataframe(pd.DataFrame(index_results), use_container_width=True)
        else:
            st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")

    # 🔍 વિભાગ ૨: ઓટો-સજેશન સર્ચ મેનુ (જ્યારે ટાઈપ કરશે ત્યારે જ ડેટા આવશે)
    st.subheader("🔍 Asset Search Menu (With Auto-Suggestions)")
    st.write("નીચે બોક્સ પર ક્લિક કરીને નામ ટાઈપ કરો, આખા લિસ્ટમાંથી **ઓટો-સજેશન** આવી જશે. સિલેક્ટ કરતા જ તેનો **Yearly હોલ ડેટા** દેખાશે.")
    
    # 💡 સ્માર્ટ સજેશન ડ્રોપડાઉન બોક્સ
    user_choice = st.selectbox(
        "સ્ટોક અથવા ઇન્ડેક્સનું નામ ટાઈપ અથવા સિલેક્ટ કરો (Search with Suggestion):",
        suggestions_pool,
        index=0
    )

    if user_choice and user_choice != "SELECT STOCK":
        search_query = user_choice.strip().upper()
        
        # સ્માર્ટ ટીકર રિઝોલ્વિંગ લોજિક
        if search_query in all_market_indices: resolved_ticker = all_market_indices[search_query]
        else: resolved_ticker = search_query + ".NS"

        with st.spinner(f"'{resolved_ticker}' નો વાર્ષિક (Yearly) સંપૂર્ણ ડેટા પ્રોસેસ થઈ રહ્યો છે..."):
            stock_res = analyze_stock_yearly(resolved_ticker)

            if stock_res:
                st.success(f"✅ '{search_query}' નો સંપૂર્ણ ડેટા મેટ્રિક્સ સફળતાપૂર્વક લોડ થઈ ગયો છે!")
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"### 📊 Historical Yearly Candle Stats")
                    st.info(f"**Live Market Spot:** ₹{stock_res['Current Price']}")
                    st.write(f"**Year Open Close:** ₹{stock_res['Open']} / ₹{stock_res['Close']}")
                    st.write(f"**Year High Bound:** ₹{stock_res['High']}")
                    st.write(f"**Year Low Bound:** ₹{stock_res['Low']}")
                    st.write(f"**Accumulated Volume:** {stock_res['Volume']:,}")
                
                with col_b:
