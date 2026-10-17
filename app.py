!pip install streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Mission 3000 MT: Terminal Friction vs. Modal Shift")

# --- SIDEBAR: INTERACTIVE CONTROLS ---
st.sidebar.header("Terminal Efficiency Upgrades")
gate_eff = st.sidebar.slider("Gate Digitization Efficiency (%)", 0, 50, 0)
crane_eff = st.sidebar.slider("Crane Handling Efficiency (%)", 0, 50, 0)
agg_eff = st.sidebar.slider("Rake Aggregation Efficiency (%)", 0, 50, 0)

# --- CALCULATIONS ---
# Base baseline delays (Delhi-Bengaluru)
base_gate = 10
base_yard = 20
base_agg = 14
fixed_transit = 16 # First/last mile road transit

# Apply slider efficiencies
new_gate = base_gate * (1 - (gate_eff/100))
new_yard = base_yard * (1 - (crane_eff/100))
new_agg = base_agg * (1 - (agg_eff/100))

total_friction_hours = fixed_transit + new_gate + new_yard + new_agg

# Logit Model Penalty Calculation
# Dynamically calculating the Alpha penalty based on total terminal hours
alpha = - (total_friction_hours / 15)

# --- PANEL 1: STACKED BAR CHART ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Terminal Friction Breakdown (Hours)")

    # Create DataFrame for plotting
    data = {'Stage': ['Origin First Mile', 'Origin Terminal', 'Dest Terminal', 'Dest Last Mile'],
            'Transit (Fixed)': [8, 0, 0, 8],
            'Gate/Docs': [0, new_gate/2, new_gate/2, 0],
            'Yard Handling': [0, new_yard/2, new_yard/2, 0],
            'Aggregation': [0, new_agg, 0, 0]}
    df = pd.DataFrame(data)

    # Plot Stacked Bar
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    df.set_index('Stage').plot(kind='bar', stacked=True, ax=ax1, color=['#2ca02c', '#d62728', '#ff7f0e', '#1f77b4'])
    ax1.set_ylabel("Hours")
    ax1.set_ylim(0, 40)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

# --- PANEL 2: S-CURVE MODAL SHIFT ---
with col2:
    st.subheader("Rail Market Share (%)")

    # Logit Math
    speeds = np.linspace(20, 75, 100)
    u_road = -12.0
    # U_rail = Alpha + (Cost_Beta * Cost) + (Time_Beta * (Distance / Speed))
    u_rail = alpha + (-0.0001 * 70000) + (-0.1 * (2100 / speeds))

    market_share = np.exp(u_rail) / (np.exp(u_rail) + np.exp(u_road)) * 100

    # Plot S-Curve
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.plot(speeds, market_share, color='blue', linewidth=3)
    ax2.set_xlabel("Average Train Speed (kmph)")
    ax2.set_ylabel("Market Share (%)")
    ax2.set_ylim(0, 100)
    ax2.axvline(x=45, color='red', linestyle='--', label='45 kmph Target')
    ax2.legend()
    st.pyplot(fig2)
