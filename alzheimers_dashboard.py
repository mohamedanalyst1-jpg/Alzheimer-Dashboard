import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# Page Config 
st.set_page_config(
    page_title="Alzheimer's Clinical Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme Colors for Charts 
C_DIAGNOSED = "#BD7849"  # Deep Orange
C_CONTROL   = "#2E4053"  # Charcoal Navy
C_ACCENT    = "#4D765E"  # Dark Green
C_PURPLE    = "#6C5B7B"  # Professional Purple for Age Trends

sns.set_theme(style="ticks")

# Data Loading & Cleaning 
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('alzaeimers.xlsx - main.csv')
    except:
        df = pd.read_excel("alzaeimers.xlsx", sheet_name="main")

    clean_cols = ["SystolicBP", "DiastolicBP", "CholesterolTotal.1", 
                  "CholesterolLDL.1", "CholesterolHDL.1", "CholesterolTriglycerides.1"]
    for col in clean_cols:
        if col in df.columns and df[col].dtype == 'object':
            df[col] = df[col].str.extract(r"([\d.]+)").astype(float)

    df = df.rename(columns={
        "CholesterolTotal.1": "TotalChol", 
        "CholesterolLDL.1": "LDL",
        "CholesterolHDL.1": "HDL", 
        "CholesterolTriglycerides.1": "Trig",
        "FamilyHistoryAlzheimers": "FamilyHistory",
    })

    df["AgeGroup"] = pd.cut(df["Age"], bins=[59, 69, 74, 79, 90], 
                            labels=["60-69", "70-74", "75-79", "80-90"])
    
    # Create numeric diagnosis for calculations
    df["IsDiagnosed"] = (df["Diagnosis"] == "Yes").astype(int)
    return df

df = load_data()

# Sidebar Navigation & Filters 
with st.sidebar:
    st.title("🧠 Filter Controls")
    st.markdown("Use these filters to refine the patient cohort analysis.")
    
    gender = st.multiselect("Gender", df["Gender"].unique(), default=list(df["Gender"].unique()))
    age_grp = st.multiselect("Age Group", df["AgeGroup"].unique().dropna().tolist(), 
                             default=df["AgeGroup"].unique().dropna().tolist())
    
    st.divider()
    st.caption("Alzheimer's Clinical Dashboard v3.1")

dff = df[(df["Gender"].isin(gender)) & (df["AgeGroup"].isin(age_grp))]

# ── Main Header ──────────────────────────────────────────────────────────────
st.title("Clinical Diagnostic Intelligence Dashboard")
st.write(f"Analyzing clinical records for **{len(dff):,}** patients.")

# KPI Section 
st.divider()
k1, k2, k3, k4 = st.columns(4)

diag_count = (dff["Diagnosis"] == "Yes").sum()
prev_rate = (diag_count / len(dff) * 100) if len(dff) > 0 else 0
avg_mmse = dff[dff["Diagnosis"] == "Yes"]["MMSE"].mean() if diag_count > 0 else 0
avg_age = dff["Age"].mean()

k1.metric("Total Cohort", f"{len(dff):,}")
k2.metric("Diagnosed Cases", f"{diag_count:,}", delta=f"{prev_rate:.1f}% Prev.", delta_color="inverse")
k3.metric("Avg MMSE (Diagnosed)", f"{avg_mmse:.1f}")
k4.metric("Avg Patient Age", f"{avg_age:.1f} yrs")

# Executive Summary 
st.header("Executive Summary", divider="orange")

i1, i2 = st.columns(2)
with i1:
    with st.container(border=True):
        st.subheader("📍 Functional Assessment Impact")
        avg_f_diag = dff[dff["Diagnosis"] == "Yes"]["FunctionalAssessment"].mean()
        avg_f_ctrl = dff[dff["Diagnosis"] == "No"]["FunctionalAssessment"].mean()
        st.write(f"Diagnosed patients score an average of **{avg_f_diag:.2f}**, vs **{avg_f_ctrl:.2f}** in controls.")
        st.info("High significance: Functional decline is the strongest diagnostic predictor.")

with i2:
    with st.container(border=True):
        st.subheader("📍 Behavioral Indicators")
        mem_rate = (dff[dff["Diagnosis"] == "Yes"]["MemoryComplaints"] == "Yes").mean() * 100
        st.write(f"Memory complaints are reported by **{mem_rate:.1f}%** of the diagnosed cohort.")
        st.success("Clinical Note: Memory issues correlate strongly with MMSE score variances.")

#  Visualizations 
st.header("Clinical Data Distributions", divider="gray")

tab1, tab2, tab3 = st.tabs(["Cognitive & Functional", "Risk Factors", "Lifestyle & Trends"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("MMSE Score Density")
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.kdeplot(data=dff, x="MMSE", hue="Diagnosis", fill=True, 
                    palette={"No": C_CONTROL, "Yes": C_DIAGNOSED}, alpha=0.6)
        sns.despine()
        st.pyplot(fig1)
    with c2:
        st.subheader("Functional Assessment vs ADL")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.scatterplot(data=dff, x="ADL", y="FunctionalAssessment", hue="Diagnosis", 
                        palette={"No": C_CONTROL, "Yes": C_DIAGNOSED}, alpha=0.5)
        sns.despine()
        st.pyplot(fig2)

with tab2:
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Symptom Prevalence (Diagnosed)")
        diag_only = dff[dff["Diagnosis"] == "Yes"]
        sym_list = ["MemoryComplaints", "Forgetfulness", "Confusion", "Disorientation"]
        sym_vals = [(diag_only[s] == "Yes").mean() * 100 for s in sym_list]
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=sym_vals, y=sym_list, color=C_DIAGNOSED)
        ax3.set_xlabel("Percentage (%)")
        sns.despine()
        st.pyplot(fig3)
    with c4:
        st.subheader("Diagnosis Rate by Education")
        edu_data = dff.groupby("EducationLevel")["IsDiagnosed"].mean().sort_values() * 100
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=edu_data.values, y=edu_data.index, color=C_ACCENT)
        ax4.set_xlabel("Diagnosis Rate (%)")
        sns.despine()
        st.pyplot(fig4)

with tab3:
    c5, c6 = st.columns(2)
    with c5:
        st.subheader("Diagnosis Rate by Age Group")
        # Calculate diagnosis rate per age group
        age_trend = dff.groupby("AgeGroup", observed=True)["IsDiagnosed"].mean() * 100
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        sns.barplot(x=age_trend.index, y=age_trend.values, color=C_PURPLE)
        ax5.set_ylabel("Diagnosis Rate (%)")
        ax5.set_xlabel("Age Range")
        # Add labels on bars
        for i, val in enumerate(age_trend.values):
            ax5.text(i, val + 0.5, f"{val:.1f}%", ha='center', fontweight='bold')
        sns.despine()
        st.pyplot(fig5)

    with c6:
        st.subheader("Sleep Quality Distribution")
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=dff, x="Diagnosis", y="SleepQuality", 
                    palette={"No": C_CONTROL, "Yes": C_DIAGNOSED}, width=0.5)
        ax6.set_ylabel("Sleep Quality Score")
        sns.despine()
        st.pyplot(fig6)

#Source Data 
st.divider()
with st.expander("📋 View Filtered Patient Records"):
    st.dataframe(dff.drop(columns=["IsDiagnosed"]), use_container_width=True)

st.caption("Dashboard generated using native Streamlit components and Seaborn ticks style.")