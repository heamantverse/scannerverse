import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

# 🖤 વેબસાઇટને કાયમી ડાર્ક મોડ અને વાઇડ લેઆઉટમાં સેટ કરવી
st.set_page_config(
    page_title="Proprietary Matrix Scanner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# કસ્ટમ CSS દ્વારા પ્રીમિયમ ડાર્ક થીમ લુક આપવો
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

# --- લૉગિન સિસ્ટમ ---
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

    # 📥 ઇન-બિલ્ટ માસ્ટર લિસ્ટ
    @st.cache_data
    def load_market_universe():
        fno_stocks = [
            "RELIANCE", "TCS", "INFY", "SBIN", "HDFCBANK", "ICICIBANK", "TATAMOTORS", "BHARTIARTL", "ITC", "HINDUNILVR",
            "LT", "BAJFINANCE", "MARUTI", "HCLTECH", "AXISBANK", "SUNPHARMA", "M&M", "TATASTEEL", "ADANIENT", "NTPC",
            "POWERGRID", "TITAN", "ULTRACEMCO", "COALINDIA", "BAJAJFINSV", "ONGC", "ADANIPORTS", "HINDALCO", "JSWSTEEL", "WIPRO",
            "NESTLEIND", "DRREDDY", "APOLLOHOSP", "SBILIFE", "BRITANNIA", "SHRIRAMFIN", "BAJAJ-AUTO", "BEL", "EICHERMOT", "HEROMOTOCO",
            "CIPLA", "DIVISLAB", "INDUSINDBK", "KOTAKBANK", "PNB", "BANKBARODA", "FEDERALBNK", "IDFCFIRSTB", "BANDHANBNK", "HAL",
            "ZOMATO", "TRENT", "VBL", "DLF", "IRFC", "RECLTD", "PFC", "IOC", "GAIL", "TATAPOWER", "CANBK", "CHOLAFIN",
            "JINDALSTEL", "AMBUJACEM", "HAVELLS", "PIDILITIND", "ADANIPOWER", "BHEL", "AUROPHARMA", "BANKINDIA", "BOSCHLTD", "DABUR",
            "DEEPAKNTR", "EXIDEIND", "GLENMARK", "GODREJPROP", "GRANULES", "GUJGASLTD", "INDIGO", "IRCTC", "JSWENERGY", "JUBLFOOD",
            "MCX", "METROPOLIS", "MFSL", "MGL", "MUTHOOTFIN", "NATIONALUM", "NAVINFLUOR", "NMDC", "OBEROIRLTY", "OFSS",
            "OIL", "PEL", "PERSISTENT", "PETRONET", "POLYCAB", "PVRINOX", "SAIL", "SUNTV", "SUPREMEIND", "TATACOMM",
            "TATAELXSI", "TATACONSUM", "TECHM", "TORNTPHARM", "TORNTPOWER", "TVSMOTOR", "UBL", "UNIONBANK", "UPL", "VOLTAS",
            "ZEEL"
        ]
        high_volume_nodes = [
            "SUZLON", "INFIBEAM", "HUDCO", "SJVN", "NHPC", "GMRINFRA", "IREDA", "PAYTM", "RVNL", "YESBANK", 
            "DELHIVERY", "MANAPPURAM", "L&TFH", "NCC", "NYKAA", "UCOBANK", "CUB", "RAMCOCEM", "SOBHA", "SONACOMS"
        ]
        return fno_stocks, high_volume_nodes

    @st.cache_data
    def load_indices_config():
        index_mapping = {
            "NIFTY 50": "^NSEI",
            "NIFTY BANK": "^NSEBANK",
            "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",
            "NIFTY IT": "^CNXIT",
            "NIFTY AUTO": "^CNXAUTO",
            "NIFTY FMCG": "^CNXFMCG",
            "NIFTY PHARMA": "^CNXPHARMA",
            "NIFTY METAL": "^CNXMETAL",
        }
        constituent_groups = {
            "NIFTY 50": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "SBIN.NS"],
            "NIFTY BANK": ["SBIN.NS", "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS"]
        }
        return index_mapping, constituent_groups

    def analyze_asset(ticker):
        try:
            df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            year_high, year_low = float(df["High"].max()), float(df["Low"].min())
            span = year_high - year_low
            current_price = float(df["Close"].iloc[-1])

            levels = {
                "Stratosphere Zone": year_low + (span * 4.236),
                "Horizon Axis": year_low + (span * 1.618),
                "Core Balance Node": year_low + (span * 0.618),
                "Ground Zero": year_low,
            }

            short_ma = df["Close"].rolling(window=5).mean().iloc[-1]
            if current_price > levels["Core Balance Node"] and current_price > short_ma:
                momentum = "Ascending Momentum Capable (🟢)"
            elif current_price < levels["Core Balance Node"] and current_price < short_ma:
                momentum = "Descending Momentum Capable (🔴)"
            else:
                momentum = "Consolidation Node (🟡)"

            closest_node = "In-Between Zones"
            min_diff = float("inf")
            for name, val in levels.items():
                diff = abs(current_price - val)
                if diff < min_diff:
                    min_diff = diff; closest_node = name

            prev_close = float(df["Close"].iloc[-2])
            prev_open = float(df["Open"].iloc[-2])
            prev_high = float(df["High"].iloc[-2])
            prev_low = float(df["Low"].iloc[-2])
            prev_volume = int(df["Volume"].iloc[-2])

            return {
                "Current Price": round(current_price, 2), "Structural Status": momentum, "Matrix Node Status": closest_node,
                "Prev Close": round(prev_close, 2), "Prev Open": round(prev_open, 2), "Prev High": round(prev_high, 2),
                "Prev Low": round(prev_low, 2), "Prev Volume": prev_volume
            }
        except: return None

    # 🛠️ એડવાન્સ મોડિફાઈડ ડીપ એન્જિન (આખા ૧૪+ સિક્રેટ લેવલ્સનો Whole Data ગણવા માટે)
    def analyze_deep_asset(ticker, timeframe):
        try:
            fetch_period = "5d" if timeframe == "Daily" else "3mo" if timeframe == "Weekly" else "1y"
            df = yf.download(ticker, period=fetch_period, auto_adjust=True, progress=False)
            if df.empty: return None
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            current_price = float(df["Close"].iloc[-1])

            if timeframe == "Daily":
                target_df = df.iloc[-2]
                o, h, l, c = float(target_df["Open"]), float(target_df["High"]), float(target_df["Low"]), float(target_df["Close"])
                v = int(target_df["Volume"])
            elif timeframe == "Weekly":
                df_weekly = df.resample("W").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"})
                target_df = df_weekly.iloc[-2]
                o, h, l, c = float(target_df["Open"]), float(target_df["High"]), float(target_df["Low"]), float(target_df["Close"])
                v = int(target_df["Volume"])
            else:
                o, h, l, c = float(df["Open"].iloc), float(df["High"].max()), float(df["Low"].min()), float(df["Close"].iloc[-1])
                v = int(df["Volume"].sum())

            span = h - l
            
            # 🎯 ઇમેજ મુજબના તમામ પોઝિટિવ અને નેગેટિવ સપ્રમાણ (Whole) લેવલ્સ
            levels = {
                "Macro Boundary High (4.236)": l + (span * 4.236),
                "Upper Multiplier Ex (3.414)": l + (span * 3.414),
                "Structural Variance High (2.618)": l + (span * 2.618),
                "Confirmation Threshold Up (2.0)": l + (span * 2.0),
                "Primary Trajectory Axis (1.618)": l + (span * 1.618),
                "Velocity Intermission Zone (1.272)": l + (span * 1.272),
                "Equilibrium Pivot Zone (0.618)": l + (span * 0.618),
                "Secondary Pivot Node (0.236)": l + (span * 0.236),
                "Anchor Baseline (0.00)": l,
                "Retraction Buffer Zone (-0.618)": l - (span * 0.618),
                "Extrapolated Range Lower (-1.618)": l - (span * 1.618),
                "Confirmation Threshold Down (-2.0)": l - (span * 2.0),
                "Structural Variance Low (-2.618)": l - (span * 2.618),
                "Lower Multiplier Ex (-3.414)": l - (span * 3.414),
                "Macro Boundary Low (-4.236)": l - (span * 4.236),
            }

            return {
                "Open": round(o, 2), "High": round(h, 2), "Low": round(l, 2), "Close": round(c, 2),
                "Volume": v, "Current Price": round(current_price, 2), "Calculated Levels": levels
            }
        except: return None

    # --- મેઈન યુઆઈ ---
    st.title("🦅 Proprietary Structural Matrix Scanner (PRO)")
    st.markdown("---")

    index_tickers, constituent_groups = load_indices_config()
    fno_list, high_vol_list = load_market_universe()

    st.sidebar.header("🎯 Filter Matrix")
    asset_class = st.sidebar.selectbox("Choose Asset Class", ["All F&O Heavyweights", "High Volume Node (>2 Lakh)"])
    selected_index = st.sidebar.selectbox("Track Index Structure", list(index_tickers.keys()))
    filter_node = st.sidebar.selectbox("Filter by Matrix Node", ["All Levels", "Stratosphere Zone", "Horizon Axis", "Core Balance Node"])

    # ૧. ઇન્ડૅક્સ ડિસ્પ્લે
    st.subheader(f"📈 Index Structure Analysis: {selected_index}")
    idx_res = analyze_asset(index_tickers[selected_index])
    if idx_res:
        c1, c2, c3 = st.columns(3)
        c1.metric("Index Spot", f"₹{idx_res['Current Price']}")
        c2.write(f"**Structural Status:** {idx_res['Structural Status']}")
        c3.write(f"**Matrix Node Status:** {idx_res['Matrix Node Status']}")

    st.markdown("---")

