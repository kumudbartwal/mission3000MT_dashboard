import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION & PROFESSIONAL DARK THEME ---
st.set_page_config(page_title="Mission 3000 MT: Freight Strategy", layout="wide")

# Custom CSS styling for a polished executive presentation look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #161b22; }
    h1, h2, h3 { color: #58a6ff; font-family: 'Helvetica Neue', sans-serif; }
    .metric-card { background-color: #21262d; padding: 15px; border-radius: 8px; border-left: 5px solid #238636; }
    </style>
""", unsafe_allow_html=True)

st.title("🚂 Dissecting Mission 3000 MT: Rail Freight Optimization Dashboard")
st.markdown("### Executive Simulation: Terminal Friction Interventions vs. Modal Shift S-Curve")

# --- SIDEBAR: STRATEGIC CAPITAL INTERVENTIONS ---
st.sidebar.header("⚙️ Strategic Intervention Levers")
st.sidebar.markdown("Adjust capital allocation to simulate operational improvements:")
gate_eff = st.sidebar.slider("Gate Digitization & Process Efficiency (%)", 0, 50, 20, help="Reduces document/gate queue times")
crane_eff = st.sidebar.slider("Terminal Crane & Yard Handling Speed (%)", 0, 50, 25, help="Speeds up container placement and lifting")
agg_eff = st.sidebar.slider("Rake Aggregation & ZBTT Timetabling (%)", 0, 50, 30, help="Reduces formation wait times and path conflicts")

# --- BASELINE VS. OPTIMIZED CALCULATIONS ---
# Baseline unoptimized hours (Delhi-NCR to Bengaluru corridor)
base_transit = 16  # Fixed first/last mile road drayage
base_gate = 10     # Gate and documentation queue
base_yard = 20     # Yard handling and crane movement
base_agg = 14      # Rake aggregation and network path waiting
baseline_total = base_transit + base_gate + base_yard + base_agg # 60 hours baseline

# Optimized hours post-intervention
opt_gate = base_gate * (1 - (gate_eff / 100))
opt_yard = base_yard * (1 - (crane_eff / 100))
opt_agg = base_agg * (1 - (agg_eff / 100))
optimized_total = base_transit + opt_gate + opt_yard + opt_agg

time_saved = baseline_total - optimized_total

# --- TOP EXECUTIVE METRICS BANNER ---
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Baseline Terminal Friction", f"{baseline_total:.1f} Hours", "Unoptimized State")
col_m2.metric("Optimized Friction", f"{optimized_total:.1f} Hours", f"-{time_saved:.1f} Hours Saved", delta_color="inverse")
col_m3.metric("Friction Reduction Gain", f"{(time_saved/baseline_total)*100:.1f}%", "Operational Efficiency")

st.markdown("---")

# --- MATPLOTLIB GLOBAL THEME SETTING FOR INFOGRAPHIC LOOK ---
plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor": "#161b22",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "xtick.color": "#c9d1d9",
    "ytick.color": "#c9d1d9",
    "text.color": "#c9d1d9",
    "grid.color": "#30363d",
    "grid.linestyle": "--"
})

# --- DUAL-PANEL EXECUTIVE INFOGRAPHIC DASHBOARD ---
col1, col2 = st.columns(2)

# --- PANEL 1: THE INFOGRAPHIC STACKED BAR (TERMINAL BREAKDOWN) ---
with col1:
    st.subheader("📊 Terminal Journey Time Breakdown")
    st.markdown("Visualizing friction reduction from Gate to Yard relative to Baseline (dashed line).")
    
    stages = ['Origin First Mile', 'Origin Terminal', 'Dest Terminal', 'Dest Last Mile']
    
    # Building structured data segments
    df_chart = pd.DataFrame({
        'Stage': stages,
        'Transit (Fixed)': [8, 0, 0, 8],
        'Gate/Docs (Red)': [0, opt_gate/2, opt_gate/2, 0],
        'Yard Handling (Orange)': [0, opt_yard/2, opt_yard/2, 0],
        'Aggregation/Path (Blue)': [0, opt_agg, 0, 0]
    })
    
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    df_chart.set_index('Stage').plot(
        kind='bar', stacked=True, ax=ax1, 
        color=['#3fb950', '#f85149', '#d29922', '#58a6ff'],
        width=0.5
    )
    
    # Adding the Baseline Reference Line across the bars
    ax1.axhline(y=baseline_total/len(stages), color='#8b949e', linestyle=':', linewidth=2, label='Baseline Threshold')
    
    ax1.set_ylabel("Hours Consumed")
    ax1.set_ylim(0, 35)
    ax1.grid(True, alpha=0.3)
    plt.xticks(rotation=25)
    ax1.legend(loc='upper right', facecolor='#21262d', edgecolor='#30363d', fontsize=9)
    st.pyplot(fig1)

# --- PANEL 2: THE MODAL SHIFT S-CURVE (LOGIT MODEL) ---
with col2:
    st.subheader("📈 Modal Shift Response (Logit S-Curve)")
    st.markdown("Demonstrating how lower terminal penalty ($\alpha$) shifts market capture to rail.")
    
    speeds = np.linspace(20, 75, 100)
    u_road = -12.0
    
    # Dynamic rail penalty derived from optimized friction hours
    alpha_optimized = - (optimized_total / 15)
    alpha_baseline = - (baseline_total / 15)
    
    u_rail_opt = alpha_optimized + (-0.0001 * 70000) + (-0.1 * (2100 / speeds))
    u_rail_base = alpha_baseline + (-0.0001 * 70000) + (-0.1 * (2100 / speeds))
    
    market_share_opt = np.exp(u_rail_opt) / (np.exp(u_rail_opt) + np.exp(u_road)) * 100
    market_share_base = np.exp(u_rail_base) / (np.exp(u_rail_base) + np.exp(u_road)) * 100
    
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    
    # Plotting both curves for visual delta comparison
    ax2.plot(speeds, market_share_opt, color='#58a6ff', linewidth=3, label='Optimized S-Curve')
    ax2.plot(speeds, market_share_base, color='#8b949e', linestyle='--', linewidth=2, label='Baseline S-Curve (Unoptimized)')
    
    ax2.set_xlabel("Door-to-Door Average Speed (kmph)")
    ax2.set_ylabel("Rail Market Share (%)")
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3)
    
    # Highlighting the 45 kmph Parity Point
    ax2.axvline(x=45, color='#f85149', linestyle='-.', alpha=0.7, label='Parity Target (45 kmph)')
    
    ax2.legend(loc='lower right', facecolor='#21262d', edgecolor='#30363d', fontsize=9)
    st.pyplot(fig2)

st.markdown("---")
st.markdown("### 💡 Executive Presentation Insights:")
st.markdown("""
* **The Fixed Anchor:** Notice how the green foundation (First/Last Mile Drayage) remains completely locked at the bottom of the bar chart, proving that road drayage is non-negotiable, while the upper blocks shrink smoothly.
* **The S-Curve Shift:** By eliminating terminal friction, the optimized S-curve shifts left relative to the grey baseline, proving that Indian Railways achieves higher market share *even at lower operating speeds* simply by removing yard and gate inefficiencies.
""")
