import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

st.set_page_config(page_title="llms.txt Generator", layout="centered")

st.title("📄 llms.txt Generator")
st.markdown("Upload a CSV with `URL`, `Title`, and `Description` columns to generate llms.txt files.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.lower().str.strip()

        required_cols = ['url', 'title', 'description']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
        else:
            df.dropna(subset=required_cols, inplace=True)
            st.success(f"File loaded with {len(df)} valid rows")
            st.dataframe(df.head())

            # llms.txt generation
            def generate_llms_txt(dataframe):
                return '\n'.join([f"- [{row['title']}]({row['url']}): {row['description']}" for _, row in dataframe.iterrows()])

            # Enhanced version
            def generate_llms_txt_with_header(dataframe, site_name="Your Website", contact_email="your-email@domain.com"):
                header = f"""# LLMs.txt for {site_name}

## About
This file contains structured information about our website content for AI systems.

## Content Overview
"""
                content = generate_llms_txt(dataframe)
                footer = f"""

## Usage Guidelines
- Please cite our website when referencing this information
- Contact: {contact_email}
- Last updated: {datetime.now().strftime('%Y-%m-%d')}
- Total pages: {len(dataframe)}
"""
                return header + content + footer

            llms_txt = generate_llms_txt(df)
            enhanced_txt = generate_llms_txt_with_header(df)

            st.download_button("⬇️ Download llms.txt", llms_txt, file_name="llms.txt")
            st.download_button("⬇️ Download Enhanced llms.txt", enhanced_txt, file_name="llms_enhanced.txt")

    except Exception as e:
        st.error(f"Error reading file: {e}")
