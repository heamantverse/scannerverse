import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# 🔒 તમારો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

st.set_page_config(layout="wide")


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

    @st.cache_data
    def load_data():
        # 🏦 ભારતના તમામ મુખ્ય ઇન્ડાઇસિસ અને તેમના અંડરલાઇંગ સ્ટોક્સનું માસ્ટર લિસ્ટ
        indices = {
            "NIFTY 50": [
                "RELIANCE.NS",
                "TCS.NS",
                "HDFCBANK.NS",
                "ICICIBANK.NS",
                "INFY.NS",
                "BHARTIARTL.NS",
                "SBIN.NS",
                "ITC.NS",
                "HINDUNILVR.NS",
                "LT.NS",
            ],
            "NIFTY BANK": [
                "SBIN.NS",
                "HDFCBANK.NS",
                "ICICIBANK.NS",
                "AXISBANK.NS",
                "KOTAKBANK.NS",
                "PNB.NS",
                "BANKBARODA.NS",
            ],
            "NIFTY FINANCIAL SERVICES": [
                "HDFCBANK.NS",
                "ICICIBANK.NS",
                "SBIN.NS",
                "AXISBANK.NS",
                "BAJFINANCE.NS",
                "CHOLAFIN.NS",
            ],
            "NIFTY IT": ["TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS", "TECHM.NS"],
            "NIFTY AUTO": [
                "TATAMOTORS.NS",
                "MARUTI.NS",
                "M&M.NS",
                "HEROMOTOCO.NS",
                "BAJAJ-AUTO.NS",
            ],
            "NIFTY FMCG": ["ITC.NS", "HINDUNILVR.NS", "NESTLEIND.NS", "BRITANNIA.NS"],
            "NIFTY PHARMA": ["SUNPHARMA.NS", "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS"],
        }

        # 🔍 ઇન્ડૅક્સના સાદા નામ અને યાહૂ ટિકર વચ્ચેનું સ્માર્ટ મેપિંગ ડિક્શનરી
        index_tickers = {
            "NIFTY 50": "^NSEI",
            "NIFTY BANK": "^NSEBANK",
            "NIFTY FINANCIAL SERVICES": "NIFTY_FIN_SERVICE.NS",
            "NIFTY IT": "^CNXIT",
            "NIFTY AUTO": "^CNXAUTO",
            "NIFTY FMCG": "^CNXFMCG",
            "NIFTY PHARMA": "^CNXPHARMA",
        }
        return indices, index_tickers

    def analyze_asset(ticker):
        try:
            df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20:
                return None
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            year_high = float(df["High"].max())
            year_low = float(df["Low"].min())
            span = year_high - year_low
            current_price = float(df["Close"].iloc[-1])

            levels = {
                "Stratosphere Zone": year_low + (span * 4.236),
                "Horizon Axis": year_low + (span * 1.618),
                "Core Balance Node": year_low + (span * 0.618),
                "Ground Zero": year_low,
            }

            short_ma = df["Close"].rolling(window=5).mean().iloc[-1]
            if (
                current_price > levels["Core Balance Node"]
                and current_price > short_ma
            ):
                momentum = "Ascending Momentum Capable (🟢)"
            elif (
                current_price < levels["Core Balance Node"]
                and current_price < short_ma
            ):
                momentum = "Descending Momentum Capable (🔴)"
            else:
                momentum = "Consolidation Node (🟡)"

            closest_node = "In-Between Zones"
            min_diff = float("inf")
            for name, val in levels.items():
                diff = abs(current_price - val)
                if diff < min_diff:
                    min_diff = diff
                    closest_node = name

            prev_close = float(df["Close"].iloc[-2])
            prev_open = float(df["Open"].iloc[-2])
            prev_high = float(df["High"].iloc[-2])
            prev_low = float(df["Low"].iloc[-2])
            prev_volume = int(df["Volume"].iloc[-2])

            return {
                "Current Price": round(current_price, 2),
                "Structural Status": momentum,
                "Matrix Node Status": closest_node,
                "Prev Close": round(prev_close, 2),
                "Prev Open": round(prev_open, 2),
                "Prev High": round(prev_high, 2),
                "Prev Low": round(prev_low, 2),
                "Prev Volume": prev_volume,
                "52W High": round(year_high, 2),
                "52W Low": round(year_low, 2),
            }
        except:
            return None

    def analyze_deep_asset(ticker, timeframe):
        try:
            if timeframe == "Daily":
                fetch_period = "5d"
            elif timeframe == "Weekly":
                fetch_period = "3mo"
            else:
                fetch_period = "1y"

            df = yf.download(ticker, period=fetch_period, auto_adjust=True, progress=False)
            if df.empty:
                return None
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            current_price = float(df["Close"].iloc[-1])

            if timeframe == "Daily":
                target_df = df.iloc[-2]
                o = float(target_df["Open"])
                h = float(target_df["High"])
                l = float(target_df["Low"])
                c = float(target_df["Close"])
                v = int(target_df["Volume"])
                high_bound, low_bound = h, l
            elif timeframe == "Weekly":
                df_weekly = df.resample("W").agg(
                    {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
                )
                target_df = df_weekly.iloc[-2]
                o = float(target_df["Open"])
                h = float(target_df["High"])
                l = float(target_df["Low"])
                c = float(target_df["Close"])
                v = int(target_df["Volume"])
                high_bound, low_bound = h, l
            else:
                o = float(df["Open"].iloc[0])
                h = float(df["High"].max())
                l = float(df["Low"].min())
                c = float(df["Close"].iloc[-1])
                v = int(df["Volume"].sum())
                high_bound, low_bound = h, l

            span = high_bound - low_bound
            levels = {
                "Stratosphere Zone": low_bound + (span * 4.236),
                "Horizon Axis": low_bound + (span * 1.618),
                "Core Balance Node": low_bound + (span * 0.618),
                "Ground Zero": low_bound,
            }

            return {
                "Open": round(o, 2),
                "High": round(h, 2),
                "Low": round(l, 2),
                "Close": round(c, 2),
                "Volume": v,
                "Current Price": round(current_price, 2),
                "Calculated Levels": levels,
            }
        except:
            return None

    # --- મેઈન ડેશબોર્ડ યુઆઈ ---
    st.title("🦅 Proprietary Structural Matrix Scanner")
    st.markdown("---")

    indices_dict, index_tickers = load_data()
    selected_index = st.sidebar.selectbox(
        "Select Index Group", list(indices_dict.keys())
    )

    filter_node = st.sidebar.selectbox(
        "Filter by Matrix Node",
        ["All Levels", "Stratosphere Zone", "Horizon Axis", "Core Balance Node"],
    )

    st.subheader(f"📈 Index Structure Analysis: {selected_index}")
    idx_res = analyze_asset(index_tickers[selected_index])
    if idx_res:
        c1, c2, c3 = st.columns(3)
        c1.metric("Index Spot", f"₹{idx_res['Current Price']}")
        c2.write(f"**Structural Status:** {idx_res['Structural Status']}")
        c3.write(f"**Matrix Node Status:** {idx_res['Matrix Node Status']}")

        st.markdown("**Index Previous Day Stats:**")
        idx_stats = pd.DataFrame(
            [
                {
                    "Open": idx_res["Prev Open"],
                    "High": idx_res["Prev High"],
                    "Low": idx_res["Prev Low"],
                    "Close": idx_res["Prev Close"],
                    "Volume": f"{idx_res['Prev Volume']:,}",
                }
            ]
        )
        st.table(idx_stats)

    st.markdown("---")

    st.subheader(f"📋 Constituent Target Matrix (With Previous Day Stats)")
    results = []
    for stock in indices_dict[selected_index]:
        res = analyze_asset(stock)
        if res:
            res["Asset Symbol"] = stock
            results.append(res)

    df_results = pd.DataFrame(results)
    if not df_results.empty:
        if filter_node != "All Levels":
            df_final = df_results[
                df_results["Matrix Node Status"].str.contains(
                    filter_node, na=False, regex=False
                )
            ]
        else:
            df_final = df_results

        if df_final.empty:
            st.warning("આ સ્તરે હાલ કોઈ ડેટા મેચ થતો નથી.")
        else:
            display_cols = [
                "Asset Symbol",
                "Current Price",
                "Structural Status",
                "Matrix Node Status",
                "Prev Open",
                "Prev High",
                "Prev Low",
                "Prev Close",
                "Prev Volume",
            ]
