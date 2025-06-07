import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(page_title="llms.txt Generator", layout="centered")

# Add caching for better performance
@st.cache_data
def process_csv(uploaded_file):
    """Cache CSV processing to avoid reprocessing on every interaction"""
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.lower().str.strip()
    return df

@st.cache_data
def generate_llms_txt_optimized(df):
    """Optimized llms.txt generation using vectorized operations"""
    # Use vectorized string operations instead of iterrows()
    content_lines = "- [" + df['title'].astype(str) + "](" + df['url'].astype(str) + "): " + df['description'].astype(str)
    return '\n'.join(content_lines.tolist())

@st.cache_data
def generate_enhanced_llms_txt(df, site_name="Your Website", contact_email="your-email@domain.com"):
    """Generate enhanced version with header and footer"""
    header = f"""# LLMs.txt for {site_name}

## About
This file contains structured information about our website content for AI systems.

## Content Overview
"""
    
    # Get optimized content
    content = generate_llms_txt_optimized(df)
    
    footer = f"""

## Usage Guidelines
- Please cite our website when referencing this information
- Contact: {contact_email}
- Last updated: {datetime.now().strftime('%Y-%m-%d')}
- Total pages: {len(df)}
"""
    
    return header + content + footer

# Main app
st.title("📄 llms.txt Generator")
st.markdown("Upload a CSV with `URL`, `Title`, and `Description` columns to generate llms.txt files.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    try:
        # Process CSV with caching
        with st.spinner("Processing CSV file..."):
            df = process_csv(uploaded_file)
        
        # Validate columns
        required_cols = ['url', 'title', 'description']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"Missing columns: {missing_cols}")
        else:
            # Clean data efficiently
            initial_count = len(df)
            df = df.dropna(subset=required_cols)
            final_count = len(df)
            
            if final_count == 0:
                st.error("No valid rows found after removing empty values.")
            else:
                st.success(f"File processed: {final_count} valid rows ({initial_count - final_count} rows removed)")
                
                # Show preview (limit to first 100 rows for performance)
                preview_df = df.head(100)
                st.dataframe(preview_df, use_container_width=True)
                
                if len(df) > 100:
                    st.info(f"Showing first 100 rows. Total rows: {len(df)}")
                
                # Generate content with progress indicator
                with st.spinner("Generating llms.txt files..."):
                    # Basic version
                    llms_txt = generate_llms_txt_optimized(df)
                    
                    # Enhanced version
                    enhanced_txt = generate_enhanced_llms_txt(df)
                
                # Download buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="⬇️ Download Basic llms.txt",
                        data=llms_txt,
                        file_name="llms.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    st.download_button(
                        label="⬇️ Download Enhanced llms.txt", 
                        data=enhanced_txt,
                        file_name="llms_enhanced.txt",
                        mime="text/plain"
                    )
                
                # Show file stats
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    st.metric("Basic File Size", f"{len(llms_txt.encode('utf-8')) / 1024:.1f} KB")
                with col3:
                    st.metric("Enhanced File Size", f"{len(enhanced_txt.encode('utf-8')) / 1024:.1f} KB")
                    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.markdown("**Common issues:**")
        st.markdown("- Make sure your CSV has the required columns: URL, Title, Description")
        st.markdown("- Check that the file is properly formatted CSV")
        st.markdown("- Ensure the file isn't corrupted")
