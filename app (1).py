import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    indices = {
        "NIFTY 50": ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "BHARTIARTL.NS", "SBIN.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS"],
        "NIFTY BANK": ["SBIN.NS", "HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "PNB.NS", "BANKBARODA.NS"]
    }
    index_tickers = {"NIFTY 50": "^NSEI", "NIFTY BANK": "^NSEBANK"}
    return indices, index_tickers

def analyze_asset(ticker):
    try:
        df = yf.download(ticker, period='1y', auto_adjust=True, progress=False)
        if df.empty or len(df) < 20: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

        year_high, year_low = float(df['High'].max()), float(df['Low'].min())
        span = year_high - year_low
        current_price = float(df['Close'].iloc[-1])

        levels = {
            "Macro Boundary High (4.236)": year_low + (span * 4.236),
            "Primary Trajectory Axis (1.618)": year_low + (span * 1.618),
            "Equilibrium Pivot Zone (0.618)": year_low + (span * 0.618),
            "Anchor Baseline (0.00)": year_low
        }

        short_ma = df['Close'].rolling(window=5).mean().iloc[-1]
        if current_price > levels["Equilibrium Pivot Zone (0.618)"] and current_price > short_ma:
            momentum = "Ascending Momentum Capable (🟢 Upside)"
        elif current_price < levels["Equilibrium Pivot Zone (0.618)"] and current_price < short_ma:
            momentum = "Descending Momentum Capable (🔴 Downside)"
        else:
            momentum = "Consolidation Node (🟡 Side-ways)"

        closest_node = "In-Between Zones"
        min_diff = float('inf')
        for name, val in levels.items():
            diff = abs(current_price - val)
            if diff < min_diff:
                min_diff = diff; closest_node = name

        return {
            "Current Price": round(current_price, 2),
            "Momentum Capability": momentum,
            "Closest Structural Node": closest_node,
            "Equilibrium Price": round(levels["Equilibrium Pivot Zone (0.618)"], 2),
            "Primary Axis Price": round(levels["Primary Trajectory Axis (1.618)"], 2)
        }
    except: return None

st.set_page_config(layout="wide")
st.title("🦅 Proprietary Structural Matrix Scanner")
st.markdown("---")

indices_dict, index_tickers = load_data()
selected_index = st.sidebar.selectbox("Select Index Group", list(indices_dict.keys()))
filter_node = st.sidebar.selectbox("Filter by Specific Fib Node", ["All Levels", "Macro Boundary High (4.236)", "Primary Trajectory Axis (1.618)", "Equilibrium Pivot Zone (0.618)"])

st.subheader(f"📈 Index Level Analysis: {selected_index}")
idx_res = analyze_asset(index_tickers[selected_index])
if idx_res:
    c1, c2, c3 = st.columns(3)
    c1.metric("Index Spot", f"₹{idx_res['Current Price']}")
    c2.write(f"**Capability:** {idx_res['Momentum Capability']}")
    c3.write(f"**Current Node:** {idx_res['Closest Structural Node']}")

st.markdown("---")
st.subheader(f"📋 Constituent Stocks under {selected_index}")
results = []
for stock in indices_dict[selected_index]:
    res = analyze_asset(stock)
    if res: res["Asset Symbol"] = stock; results.append(res)

df_results = pd.DataFrame(results)
if not df_results.empty:
    if filter_node != "All Levels":
        df_final = df_results[df_results["Closest Structural Node"].str.contains(filter_node, na=False, regex=False)]
    else: df_final = df_results

    if df_final.empty: st.warning("આ લેવલ પર હાલ કોઈ સ્ટોક નથી.")
    else: st.dataframe(df_final[["Asset Symbol", "Current Price", "Momentum Capability", "Closest Structural Node", "Equilibrium Price", "Primary Axis Price"]], use_container_width=True)

st.markdown("---")
st.caption("⚠️ Disclaimer: Educational mathematical matrix. Not SEBI registered. Cross-verify with live broker charts before assessment.")
