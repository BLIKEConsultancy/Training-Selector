
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BLIKE Training Selector", layout="wide")
st.image("Blike Logo.png", width=200)

st.title("📚 BLIKE Training Selector Tool")

# Google Sheet CSV export URL (live link)
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhIrxnV8slbiNOox7qylKhAw6lnC94tuT3SM1CPmAOZ6HV1HjfYCPqRpADML64Aw/pub?output=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(sheet_url)
    return df

df = load_data()

# Filters
st.sidebar.header("🔍 Filter Trainings")
date_filter = st.sidebar.date_input("Date (optional)", value=None)
cert_filter = st.sidebar.selectbox("Certificate Offered?", options=["All", "Yes", "No"])
search_term = st.sidebar.text_input("Search by Title/Description")

filtered_df = df.copy()
if cert_filter != "All":
    filtered_df = filtered_df[filtered_df["Certificate"].str.lower() == cert_filter.lower()]
if search_term:
    filtered_df = filtered_df[
        filtered_df["Title"].str.contains(search_term, case=False, na=False) |
        filtered_df["Description"].str.contains(search_term, case=False, na=False)
    ]

# Display table
st.subheader("Available Trainings")
for _, row in filtered_df.iterrows():
    with st.container():
        st.markdown(f"### {row['Title']}")
        st.markdown(f"**Date:** {row['Date']}")
        st.markdown(f"**Description:** {row['Description']}")
        st.markdown(f"**Certificate:** {row['Certificate']}")
        enroll_link = f"mailto:katrinidad@blike.com.ph?subject=Training Enrollment: {row['Title']}"
        st.markdown(f"[📩 Enroll Now]({enroll_link})", unsafe_allow_html=True)
        st.markdown("---")
