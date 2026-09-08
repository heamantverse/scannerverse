import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# 🔒 તમારો નવો પાવરફુલ સિક્રેટ પાસવર્ડ
CORRECT_PASSWORD = "PowerFULLtrade"

st.set_page_config(layout="wide")


# --- લૉગિન સિસ્ટમ ફંક્શન ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔒 Security Access Required")
        st.write("આ એક પ્રાઇવેટ પ્રોપ્રાઇટરી મેટ્રિક્સ સ્કેનર છે.")

        # પાસવર્ડ ઇનપુટ બોક્સ
        user_password = st.text_input("Enter Private Access Password:", type="password")

        if st.button("Access Dashboard"):
            if user_password == CORRECT_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ ખોટો પાસવર્ડ! એક્સેસ નકારવામાં આવ્યો છે.")
        return False
    return True


# પાસવર્ડ વેરિફિકેશન પછી જ મેઈન ડેશબોર્ડ ખૂલશે
if check_password():

    @st.cache_data
    def load_data():
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
        }
        index_tickers = {"NIFTY 50": "^NSEI", "NIFTY BANK": "^NSEBANK"}
        return indices, index_tickers

    def analyze_asset(ticker):
        try:
            df = yf.download(ticker, period="1y", auto_adjust=True, progress=False)
            if df.empty or len(df) < 20:
                return None
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

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

            return {
                "Current Price": round(current_price, 2),
                "Structural Status": momentum,
                "Matrix Node Status": closest_node,
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

    st.markdown("---")
    st.subheader(f"📋 Constituent Target Matrix")
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
            st.dataframe(
                df_final[
                    [
                        "Asset Symbol",
                        "Current Price",
                        "Structural Status",
                        "Matrix Node Status",
                    ]
                ],
                use_container_width=True,
            )

    st.markdown("---")
    st.caption(
        "⚠️ Disclaimer: Educational proprietary structural matrix. Not SEBI registered."
    )

    # સાઇડબાર લોગઆઉટ બટન
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()
