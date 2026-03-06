import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Data Autopilot", layout="wide")

# Title
st.title("🚀 AI Data Autopilot")
st.write("Upload your data or test with sample data")

# ============================================
# SIDEBAR: Load Data
# ============================================
st.sidebar.header("Load Data")

# Checkbox to use sample data
use_sample = st.sidebar.checkbox("Use Sample Data?", value=True)

df = None

if use_sample:
    # Load sample data
    try:
        df = pd.read_csv("sample_data/subscription_data.csv")
        st.sidebar.success("✓ Loaded sample data")
    except FileNotFoundError:
        st.sidebar.error("❌ Sample data not found. Run: python generate_sample_data.py")

else:
    # User uploads their own CSV
    uploaded_file = st.sidebar.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✓ Loaded {uploaded_file.name}")

# ============================================
# MAIN CONTENT
# ============================================

if df is not None:
    # Show success
    st.subheader("✓ Data Loaded Successfully")
    
    # Basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    
    # Show column information
    st.subheader("Column Information")
    col_info = pd.DataFrame({
        'Column': df.columns,
        'Type': df.dtypes.astype(str),
        'Non-Null': df.count(),
        'Null': df.isnull().sum()
    })
    st.dataframe(col_info, use_container_width=True)
    
    # Show preview of data
    st.subheader("Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Show basic statistics
    st.subheader("Basic Statistics")
    st.dataframe(df.describe(), use_container_width=True)

else:
    st.info("Check 'Use Sample Data?' to get started, or upload your own CSV file")