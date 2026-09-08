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
    # ૫ મુખ્ય ઇન્ડાઇસિસનું ફિક્સ ડિક્શનરી
    main_5_indices = {
        "NIFTY 50": "^NSEI",
        "NIFTY BANK": "^NSEBANK",
        "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",
        "NIFTY IT": "^CNXIT",
        "NIFTY AUTO": "^CNXAUTO"
    }

    # ⏳ લોજિક ૧: ઇન્ડૅક્સ માટે પ્યોર DAILY બેઝ એનાલિસિસ ફંક્શન
    def analyze_index_daily(ticker_name, display_name):
        try:
            df = yf.download(ticker_name, period="5d", auto_adjust=True, progress=False)
            if df.empty or len(df) < 2: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
            # ગઈકાલની ડેઇલી કેન્ડલનો હાઇ-લો ડેટા
            target_df = df.iloc[-2]
            h, l, c = float(target_df["High"]), float(target_df["Low"]), float(target_df["Close"])
            current_price = float(df["Close"].iloc[-1])
            span = h - l
            
            # ડેઇલી ફિબોનાચી સિક્રેટ લેવલ્સ
            levels = {
                "Stratosphere Zone": l + (span * 4.236),
                "Horizon Axis": l + (span * 1.618),
                "Core Balance Node": l + (span * 0.618),
                "Ground Zero": l
            }
            
            # લાઈવ ભાવથી સૌથી નજીક (Nearby) કયું લેવલ છે તે શોધવું
            closest_node = "In-Between Zones"
            min_diff = float("inf")
            for name, val in levels.items():
                diff = abs(current_price - val)
                if diff < min_diff:
                    min_diff = diff
                    closest_node = name
            
            return {
                "Index Name": display_name,
                "Current Price": round(current_price, 2),
                "Nearby Structural Node": closest_node
            }
        except: return None

    # 📈 લોજિક ૨: સ્ટોક્સ માટે પ્યોર YEARLY બેઝ એનાલિસિસ ફંક્શન (સર્ચ મેનુ માટે)
    def analyze_stock_yearly(ticker_name):
        try:
            df = yf.download(ticker_name, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            
            # આખા ૧ વર્ષનો મેક્સિમમ હાઇ-લો ડેટા
            year_high, year_low = float(df["High"].max()), float(df["Low"].min())
            current_price = float(df["Close"].iloc[-1])
            span = year_high - year_low
            
            # વાર્ષિક ૧૫ એ ૧૫ સિક્રેટ ફિબોનાચી લેવલ્સનો આખો ડેટા (Whole Data)
            levels = {
                "Stratosphere Matrix Max (4.236)": year_low + (span * 4.236),
                "Stratosphere Boundary (3.414)": year_low + (span * 3.414),
                "Stratosphere Core (2.618)": year_low + (span * 2.618),
                "Upper Conformation Threshold (2.0)": year_low + (span * 2.0),
                "Horizon Axis (1.618)": year_low + (span * 1.618),
                "Velocity Intermission Zone (1.272)": year_low + (span * 1.272),
                "Core Balance Node (0.618)": year_low + (span * 0.618),
                "Secondary Pivot Node (0.236)": year_low + (span * 0.236),
                "Ground Zero Base (0.00)": year_low,
                "Retraction Buffer Zone (-0.618)": year_low - (span * 0.618),
                "Extrapolated Range Lower (-1.618)": year_low - (span * 1.618),
                "Lower Conformation Threshold (-2.0)": year_low - (span * 2.0),
                "Structural Variance Low (-2.618)": year_low - (span * 2.618),
                "Lower Multiplier Ex (-3.414)": year_low - (span * 3.414),
                "Macro Boundary Low (-4.236)": year_low - (span * 4.236),
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

    # --- મેઈન યુઆઈ લેઆઉટ ---
    st.title("🦅 Proprietary Structural Matrix Scanner (PRO)")
    st.markdown("---")

    # 📊 વિભાગ ૧: મેઈન પેજ પર ફક્ત ૫ મુખ્ય ઇન્ડાઇસિસનો Nearby ડેટા
    st.subheader("📈 Main Index Track List (Daily Base Nearby Matrix)")
    st.write("આ ઇન્ડાઇસિસનો ડેટા પ્યોર **Daily બેઝ** પરથી ગણવામાં આવ્યો છે અને અત્યારના ભાવની **સૌથી નજીકનું લેવલ** બતાવે છે.")
    
    with st.spinner("ઇન્ડાઇસિસ મેટ્રિક્સ લોડ થઈ રહ્યો છે..."):
        index_results = []
        for name, ticker in main_5_indices.items():
            res = analyze_index_daily(ticker, name)
            if res: index_results.append(res)
        
        if len(index_results) > 0:
            st.dataframe(pd.DataFrame(index_results), use_container_width=True)
        else:
            st.warning("ઇન્ડૅક્સ ડેટા લોડ થઈ શક્યો નથી.")

    st.markdown("---")

    # 🔍 વિભાગ ૨: ડેડિકેટેડ સર્ચ મેનુ (બીજો કોઈ પણ ડેટા ડાયરેક્ટ લોડ નહીં થાય)
    st.subheader("🔍 Asset Search Menu (Yearly Whole Data Analysis)")
    st.write("કોઈપણ સ્ટોક (e.g. TCS, SUZLON, TATAPOWER, SBIN) નું નામ લખીને એન્ટર કરો. તેનો **આખા ૧ વર્ષનો ડેટા મેટ્રિક્સ** નીચે લોડ થશે.")
    
    # ⌨️ સંપૂર્ણ ખાલી સર્ચ બોક્સ (ડિફોલ્ટ કંઈ જ લોડ નહીં થાય)
    user_search = st.text_input("સ્ટોક અથવા ઇન્ડેક્સનો સિમ્બોલ ટાઈપ કરો અને Enter દબાવો:", "")

    if user_search:
        search_query = user_search.strip().upper()
        
        # જો યુઝર સર્ચ બોક્સમાં ઇન્ડેક્સનું નામ લખે
        if search_query in main_5_indices: resolved_ticker = main_5_indices[search_query]
        elif search_query in ["NIFTY50", "NIFTY 50"]: resolved_ticker = "^NSEI"
        elif search_query in ["BANKNIFTY", "NIFTY BANK"]: resolved_ticker = "^NSEBANK"
        else: resolved_ticker = search_query if search_query.endswith(".NS") or search_query.startswith("^") else search_query + ".NS"

        with st.spinner(f"'{resolved_ticker}' નો વાર્ષિક (Yearly) હોલ ડેટા પ્રોસેસ થઈ રહ્યો છે..."):
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
                    st.markdown(f"### 🦅 Complete Symmetrical Matrix (1-Year Levels)")
                    # ૧૫ એ ૧૫ એડવાન્સ સિક્રેટ લેવલ્સનો આખો ડેટા કિંમત સાથે બતાવવો
                    for lvl_name, lvl_val in stock_res["Calculated Levels"].items():
                        st.write(f"**{lvl_name}:** ₹{lvl_val:.2f}")
            else:
                st.error(f"❌ '{user_search}' નામનો કોઈ સ્ટોક કે ઇન્ડેક્સ મળ્યો નથી. કૃપા કરીને સાચો NSE Symbol લખો.")
    else:
        st.info("💡 સર્ચ બોક્સમાં સ્ટોકનું નામ લખો, અત્યારે નીચે કોઈ ડેટા લોડ કરેલો નથી.")

    st.markdown("---")
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()
