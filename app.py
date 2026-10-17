import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIGURATION & EXECUTIVE THEME ---
st.set_page_config(page_title="Mission 3000 MT: Freight Strategy", layout="wide")

# Custom refined CSS styling for compact typography, rounded cards, and color-matched sliders
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #c9d1d9; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    h1 { color: #58a6ff; font-size: 1.8rem; font-weight: 600; margin-bottom: 0.1rem; }
    h2, h3 { color: #58a6ff; font-size: 1.2rem; font-weight: 500; }
    p, label, span { font-size: 0.9rem; color: #8b949e; }
    
    /* Control Box Styling with Color Accents */
    .control-box-green { background: #161b22; padding: 12px; border-radius: 10px; border-top: 4px solid #3fb950; border-left: 1px solid #30363d; border-right: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .control-box-red { background: #161b22; padding: 12px; border-radius: 10px; border-top: 4px solid #f85149; border-left: 1px solid #30363d; border-right: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .control-box-orange { background: #161b22; padding: 12px; border-radius: 10px; border-top: 4px solid #d29922; border-left: 1px solid #30363d; border-right: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    .control-box-blue { background: #161b22; padding: 12px; border-radius: 10px; border-top: 4px solid #58a6ff; border-left: 1px solid #30363d; border-right: 1px solid #30363d; border-bottom: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

st.title("🚂 Mission 3000 MT: Rail Freight Optimization Dashboard")
st.markdown("<p style='margin-top:0px;'>Executive Decision Support System: Simulating Terminal Friction vs. Modal Shift S-Curve</p>", unsafe_allow_html=True)

# --- BASELINE VS. OPTIMIZED CALCULATIONS ---
base_transit = 16  # Fixed first/last mile road drayage
base_gate = 10     # Gate and documentation queue
base_yard = 20     # Yard handling and crane movement
base_agg = 14      # Rake aggregation and network path waiting
baseline_total = base_transit + base_gate + base_yard + base_agg # 60 hours baseline

# --- MATPLOTLIB GLOBAL THEME FOR REFINED INFOGRAPHIC LOOK ---
plt.rcParams.update({
    "figure.facecolor": "#0e1117",
    "axes.facecolor": "#161b22",
    "axes.edgecolor": "#30363d",
    "axes.labelcolor": "#c9d1d9",
    "xtick.color": "#c9d1d9",
    "ytick.color": "#c9d1d9",
    "text.color": "#c9d1d9",
    "grid.color": "#21262d",
    "grid.linestyle": "--",
    "font.sans-serif": "Helvetica",
    "font.size": 9
})

# --- DUAL-PANEL EXECUTIVE INFOGRAPHIC DASHBOARD (TOP) ---
col1, col2 = st.columns(2)

# Global variables placeholder controlled by sliders below
if 'gate_eff' not in st.session_state: st.session_state.gate_eff = 20
if 'crane_eff' not in st.session_state: st.session_state.crane_eff = 25
if 'agg_eff' not in st.session_state: st.session_state.agg_eff = 30

opt_gate = base_gate * (1 - (st.session_state.gate_eff / 100))
opt_yard = base_yard * (1 - (st.session_state.crane_eff / 100))
opt_agg = base_agg * (1 - (st.session_state.agg_eff / 100))
optimized_total = base_transit + opt_gate + opt_yard + opt_agg
time_saved = baseline_total - optimized_total

# --- PANEL 1: THE EVOLVED ROUNDED BAR CHART ---
with col1:
    st.subheader("📊 Terminal Journey Time Breakdown")
    
    stages = ['Origin First Mile', 'Origin Terminal', 'Dest Terminal', 'Dest Last Mile']
    
    df_chart = pd.DataFrame({
        'Stage': stages,
        'Transit (Fixed)': [8, 0, 0, 8],
        'Gate/Docs': [0, opt_gate/2, opt_gate/2, 0],
        'Yard Handling': [0, opt_yard/2, opt_yard/2, 0],
        'Aggregation/Path': [0, opt_agg, 0, 0]
    })
    
    fig1, ax1 = plt.subplots(figsize=(6, 3.8))
    
    # Plotting with rounded bar styling via edge properties and alpha
    bars = df_chart.set_index('Stage').plot(
        kind='bar', stacked=True, ax=ax1, 
        color=['#3fb950', '#f85149', '#d29922', '#58a6ff'],
        width=0.45, edgecolor='#0e1117', linewidth=1.5
    )
    
    # Softening bar corners visually
    for container in ax1.containers:
        for bar in container:
            bar.set_antialiased(True)

    ax1.axhline(y=baseline_total/len(stages), color='#8b949e', linestyle=':', linewidth=1.5, label='Baseline Threshold')
    
    ax1.set_ylabel("Hours Consumed", fontsize=8)
    ax1.set_ylim(0, 32)
    ax1.grid(True, alpha=0.2)
    plt.xticks(rotation=20, fontsize=8)
    ax1.legend(loc='upper right', facecolor='#161b22', edgecolor='#30363d', fontsize=7)
    plt.tight_layout()
    st.pyplot(fig1)

# --- PANEL 2: THE MODAL SHIFT S-CURVE (LOGIT MODEL) ---
with col2:
    st.subheader("📈 Modal Shift Response (Logit S-Curve)")
    
    speeds = np.linspace(20, 75, 100)
    u_road = -12.0
    
    alpha_optimized = - (optimized_total / 15)
    alpha_baseline = - (baseline_total / 15)
    
    u_rail_opt = alpha_optimized + (-0.0001 * 70000) + (-0.1 * (2100 / speeds))
    u_rail_base = alpha_baseline + (-0.0001 * 70000) + (-0.1 * (2100 / speeds))
    
    market_share_opt = np.exp(u_rail_opt) / (np.exp(u_rail_opt) + np.exp(u_road)) * 100
    market_share_base = np.exp(u_rail_base) / (np.exp(u_rail_base) + np.exp(u_road)) * 100
    
    fig2, ax2 = plt.subplots(figsize=(6, 3.8))
    
    ax2.plot(speeds, market_share_opt, color='#58a6ff', linewidth=2.5, label='Optimized S-Curve')
    ax2.plot(speeds, market_share_base, color='#8b949e', linestyle='--', linewidth=1.5, label='Baseline S-Curve')
    
    ax2.set_xlabel("Average Speed (kmph)", fontsize=8)
    ax2.set_ylabel("Rail Market Share (%)", fontsize=8)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.2)
    
    ax2.axvline(x=45, color='#f85149', linestyle='-.', alpha=0.7, label='Parity Target (45 kmph)')
    ax2.legend(loc='lower right', facecolor='#161b22', edgecolor='#30363d', fontsize=7)
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown("---")

# --- INTERACTIVE CONTROLS PLACED BELOW WITH COLOR-MATCHED THEMES ---
st.markdown("### 🎛️ Interactive Intervention Levers (Adjust Parameters)")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="control-box-red">', unsafe_allow_html=True)
    st.session_state.gate_eff = st.slider("Gate Digitization Efficiency (%)", 0, 50, st.session_state.gate_eff)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="control-box-orange">', unsafe_allow_html=True)
    st.session_state.crane_eff = st.slider("Terminal Crane Handling Speed (%)", 0, 50, st.session_state.crane_eff)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="control-box-blue">', unsafe_allow_html=True)
    st.session_state.agg_eff = st.slider("Rake Aggregation & ZBTT (%)", 0, 50, st.session_state.agg_eff)
    st.markdown('</div>', unsafe_allow_html=True)

