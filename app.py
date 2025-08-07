
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BLIKE Training Selector", layout="wide")
st.image("Blike Logo.png", width=200)

st.title("📚 BLIKE Training Selector Tool")

# Google Sheet CSV export URL (live link)
sheet_url = "https://docs.google.com/spreadsheets/d/15L9FQ-zaTho749GmoawJXsPaaPa0KciRbQqHxI8b9Wg/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(sheet_url)
    return df

df = load_data()

# Strip leading/trailing spaces from column names
#df.columns = df.columns.str.strip()

# Optional: show column names for debugging
#st.write(df.columns.tolist())

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
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"**Level:** {row['Level']}")
        st.markdown(f"**Date:** {row['Date']}")
        st.markdown(f"**Certificate:** {row['Certificate']}")
        st.markdown(f"**New:** {row['New']}")
        st.markdown(f"**Description:** {row['Description']}")
        st.markdown(f"**Price:** {row['Price']}")

        with st.expander("📋 Enroll Now"):
            name = st.text_input(f"Your Name for {row['Title']}", key=f"name_{row['Title']}")
            email = st.text_input(f"Your Email", key=f"email_{row['Title']}")
            phone = st.text_input(f"Your Phone Number", key=f"phone_{row['Title']}")

            if st.button(f"📩 Confirm Enrollment", key=f"enroll_{row['Title']}"):
                if name and email:
                    subject = f"Training Enrollment: {row['Title']}"
                    body = (
                        f"Hi,\n\n"
                        f"I would like to enroll in the training titled \"{row['Title']}\".\n\n"
                        f"Name: {name}\n"
                        f"Email: {email}\n"
                        f"Phone: {phone}\n\n"
                        f"Thank you!"
                    )
                    mailto_link = f"mailto:katrinidad@blike.com.ph?subject={subject}&body={body}"
                    mailto_link = mailto_link.replace('\n', '%0D%0A')  # line breaks for mail body

                    st.markdown(
                        f'<meta http-equiv="refresh" content="0; url={mailto_link}">',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("Please fill in at least your name and email to proceed.")

        st.markdown("---")
