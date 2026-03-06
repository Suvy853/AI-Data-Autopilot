import streamlit as st
import pandas as pd
from src.data_loader import load_csv, check_data_quality, clean_data

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
    try:
        df = load_csv("sample_data/subscription_data.csv")
        quality_report = check_data_quality(df)
        st.sidebar.success("✓ Loaded sample data")
        df = clean_data(df, quality_report)
        
    except FileNotFoundError:
        st.sidebar.error("❌ Sample data not found")
        df = None

else:
    uploaded_file = st.sidebar.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Use pd.read_csv directly for uploaded files (not load_csv)
            df = pd.read_csv(uploaded_file)
            
            # Check quality
            quality_report = check_data_quality(df)
            st.sidebar.success(f"✓ Loaded {uploaded_file.name}")
            
            # Clean the data
            df = clean_data(df, quality_report)
            
        except Exception as e:
            st.sidebar.error(f"❌ Error: {e}")
            df = None
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

# QUALITY REPORT SECTION 
    st.subheader("📊 Data Quality Report")
    
    quality_report = check_data_quality(df)
    
    # Show quality metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Quality Score", f"{quality_report['quality_score']:.1f}%")
    with col2:
        st.metric("Blank Cells", quality_report['blank_cells'])
    with col3:
        st.metric("Duplicate Rows", quality_report['duplicate_rows'])
    with col4:
        st.metric("Column Types Detected", len(quality_report['column_types']))
    
    # Show issues if any
    if quality_report['issues']:
        st.warning("⚠️ Issues Found:")
        for issue in quality_report['issues']:
            st.write(f"  • {issue}")
    else:
        st.success("✓ No major quality issues found")        
    
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


if use_sample:
    try:
        df = load_csv("sample_data/subscription_data.csv")
        
        # Check quality
        quality_report = check_data_quality(df)
        st.sidebar.success("✓ Loaded sample data")
        
        # Show quality before cleaning
        st.sidebar.write(f"**Quality Score**: {quality_report['quality_score']:.1f}%")
        
        # Clean the data
        df = clean_data(df, quality_report)
        
    except Exception as e:
        st.sidebar.error(f"❌ Error: {e}")
        df = None    