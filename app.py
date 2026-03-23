import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import load_csv, check_data_quality, clean_data
from src.kpi_engine import detect_metric_columns, calculate_basic_kpis, calculate_trends, analyze_by_segment
from src.anomaly import detect_statistical_outliers, detect_isolation_forest_outliers
from src.narrative_enhanced import (detect_important_segments, 
                                    generate_business_insights, 
                                    generate_business_recommendations)
from src.report import generate_pdf_report, export_kpis_to_csv, export_anomalies_to_csv, export_recommendations_to_csv

# Page configuration
st.set_page_config(page_title="AI Data Autopilot", layout="wide", initial_sidebar_state="expanded")

# ============================================
# HEADER
# ============================================
st.title("AI Data Autopilot")
st.write("Executive Data Quality Dashboard - Understand your data before deep analysis")

# ============================================
# SIDEBAR - LOAD DATA
# ============================================
with st.sidebar:
    st.header("Load Data")
    
    use_sample = st.checkbox("Use Sample Data?", value=True, key="use_sample_data")
    
    df = None
    df_original = None
    quality_report = None
    
    if use_sample:
        try:
            df_original = load_csv("sample_data/subscription_data.csv")
            quality_report = check_data_quality(df_original)
            df = clean_data(df_original.copy(), quality_report)
            st.success("Sample data loaded successfully")
        except FileNotFoundError:
            st.error("Sample data file not found")
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type="csv", key="csv_uploader")
        if uploaded_file is not None:
            try:
                df_original = pd.read_csv(uploaded_file)
                quality_report = check_data_quality(df_original)
                df = clean_data(df_original.copy(), quality_report)
                st.success(f"{uploaded_file.name} loaded successfully")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # ============================================
    # SIDEBAR - NAVIGATION
    # ============================================
    st.sidebar.markdown("---")
    st.sidebar.header("Dashboard Sections")
    st.sidebar.info("""
    1. Data Overview
    2. Data Cleaning
    3. KPI Analysis
    4. Segment Analysis
    5. Anomaly Detection
    6. Business Insights
    7. Recommendations
    8. Reports & Exports
    """)

# ============================================
# MAIN CONTENT
# ============================================

if df is not None and df_original is not None and quality_report is not None:
    
    # ============================================
    # SECTION 1: DATA OVERVIEW
    # ============================================
    st.header("Step 1: Data Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        quality_score = quality_report['quality_score']
        st.metric("Quality Score", f"{quality_score:.1f}%")
    with col4:
        st.metric("Data Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # Quality assessment details
    st.subheader("Data Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        blank_cells = quality_report['blank_cells']
        st.write(f"**Blank Cells:** {blank_cells:,}")
        if blank_cells == 0:
            st.success("No missing data")
        else:
            st.warning(f"{blank_cells} values need attention")
    
    with col2:
        duplicates = quality_report['duplicate_rows']
        st.write(f"**Duplicate Rows:** {duplicates}")
        if duplicates == 0:
            st.success("No duplicates")
        else:
            st.warning(f"{duplicates} duplicate rows detected")
    
    with col3:
        st.write(f"**Data Issues:** {len(quality_report['issues'])}")
        if len(quality_report['issues']) == 0:
            st.success("No issues detected")
        else:
            for issue in quality_report['issues']:
                st.info(issue)

    # ============================================
    # SECTION 2: DATA CLEANING
    # ============================================
    st.header("Step 2: Data Cleaning")
    
    tab1, tab2, tab3 = st.tabs(["Summary", "Before", "After"])
    
    with tab1:
        st.subheader("Cleaning Applied")
        
        original_blanks = df_original.isnull().sum().sum()
        cleaned_blanks = df.isnull().sum().sum()
        blanks_removed = original_blanks - cleaned_blanks
        
        original_dups = len(df_original) - len(df_original.drop_duplicates())
        cleaned_dups = len(df) - len(df.drop_duplicates())
        dups_removed = original_dups - cleaned_dups
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Blanks Filled", blanks_removed)
        with col2:
            st.metric("Duplicates Removed", dups_removed)
        with col3:
            quality_before = check_data_quality(df_original)['quality_score']
            quality_after = quality_report['quality_score']
            st.metric("Quality Improvement", f"+{quality_after - quality_before:.1f}%")
    
    with tab2:
        st.write("### Original Data (Before Cleaning)")
        st.dataframe(df_original.head(10), use_container_width=True)
    
    with tab3:
        st.write("### Cleaned Data (After Cleaning)")
        st.dataframe(df.head(10), use_container_width=True)

    # ============================================
    # SECTION 3: KPI ANALYSIS
    # ============================================
    st.header("Step 3: KPI Analysis")
    
    try:
        metrics = detect_metric_columns(df)
        
        if metrics:
            kpis = calculate_basic_kpis(df, metrics)
            
            st.write(f"**Auto-Detected {len(kpis)} Key Metrics**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("KPI Summary")
                kpi_df = pd.DataFrame(kpis).T[['average', 'sum', 'min', 'max']]
                st.dataframe(kpi_df, use_container_width=True)
            
            with col2:
                st.subheader("KPI Comparison - Bar Chart")
                kpi_averages = {col: values['average'] for col, values in kpis.items()}
                fig_bar = px.bar(
                    x=list(kpi_averages.keys()),
                    y=list(kpi_averages.values()),
                    labels={'x': 'Metric', 'y': 'Average Value'},
                    title="Average Values by Metric",
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No numeric columns found for KPI analysis")
    except Exception as e:
        st.error(f"Error in KPI analysis: {e}")

    # ============================================
    # SECTION 4: SEGMENT ANALYSIS
    # ============================================
    st.header("Step 4: Segment Performance Analysis")
    
    try:
        segments = detect_important_segments(df, metrics if metrics else {})
        
        if segments:
            st.write("**Auto-Detected Customer Segments**")
            
            for segment_col, segment_data in segments.items():
                st.subheader(f"Segment: {segment_col}")
                
                segment_display = []
                for seg_name, seg_info in segment_data.items():
                    segment_display.append({
                        'Segment': seg_name,
                        'Count': seg_info['count'],
                        'Percentage': f"{seg_info['percentage']:.1f}%"
                    })
                
                segment_df = pd.DataFrame(segment_display).sort_values('Count', ascending=False)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(segment_df, use_container_width=True)
                
                with col2:
                    # Bar chart instead of pie chart
                    fig_bar = px.bar(
                        segment_df,
                        x='Segment',
                        y='Count',
                        title=f"Segment Distribution: {segment_col}",
                        labels={'Count': 'Number of Records'},
                        color='Count',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No clear segments detected in this dataset")
    except Exception as e:
        st.error(f"Error in segment analysis: {e}")

    # ============================================
    # SECTION 5: ANOMALY DETECTION
    # ============================================
    st.header("Step 5: Anomaly Detection (Quality Check)")
    
    st.info("""
    Two Detection Methods:
    - Z-Score: Statistical outliers (greater than 3 standard deviations from mean)
    - Isolation Forest: ML-based multivariate anomalies
    """)
    
    try:
        numeric_cols = list(metrics.keys()) if metrics else []
        
        if numeric_cols:
            anomaly_tab1, anomaly_tab2, anomaly_tab3 = st.tabs(
                ["Z-Score Analysis", "ML-Based Analysis", "Summary"]
            )
            
            # Z-Score Anomalies
            with anomaly_tab1:
                st.subheader("Statistical Outliers (Z-Score)")
                
                all_z_anomalies = []
                for col in numeric_cols[:3]:
                    outliers = detect_statistical_outliers(df, col)
                    if len(outliers) > 0:
                        all_z_anomalies.append(outliers)
                
                if all_z_anomalies:
                    z_anomalies = pd.concat(all_z_anomalies, ignore_index=True)
                    st.warning(f"Found {len(z_anomalies)} statistical outliers")
                    
                    z_display = z_anomalies.copy()
                    if 'z_score' in z_display.columns:
                        z_display['Severity'] = z_display['z_score'].apply(
                            lambda x: 'Critical' if abs(x) > 4 else 'High' if abs(x) > 3 else 'Medium'
                        )
                    
                    st.dataframe(z_display.head(15), use_container_width=True)
                    
                    # Histogram of z-scores
                    fig_hist = px.histogram(
                        z_display,
                        x='z_score',
                        nbins=30,
                        title='Distribution of Z-Scores',
                        labels={'z_score': 'Z-Score Value', 'count': 'Frequency'}
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.success("No statistical outliers detected")
            
            # ML Anomalies
            with anomaly_tab2:
                st.subheader("ML-Based Anomalies (Isolation Forest)")
                
                anomalies_ml = detect_isolation_forest_outliers(df, numeric_cols)
                
                if len(anomalies_ml) > 0:
                    anomaly_pct = (len(anomalies_ml) / len(df)) * 100
                    st.warning(f"Found {len(anomalies_ml)} anomalous records ({anomaly_pct:.2f}%)")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Horizontal bar chart instead of pie
                        anomaly_stats = {
                            'Normal': len(df) - len(anomalies_ml),
                            'Anomalous': len(anomalies_ml)
                        }
                        fig_hbar = px.bar(
                            x=list(anomaly_stats.values()),
                            y=list(anomaly_stats.keys()),
                            orientation='h',
                            title="Data Classification",
                            labels={'x': 'Count', 'y': 'Type'},
                            color=list(anomaly_stats.keys()),
                            color_discrete_map={'Normal': '#3498db', 'Anomalous': '#e74c3c'}
                        )
                        st.plotly_chart(fig_hbar, use_container_width=True)
                    
                    with col2:
                        if anomaly_pct < 1:
                            st.success(f"Excellent: {anomaly_pct:.2f}% anomalies")
                        elif anomaly_pct < 5:
                            st.info(f"Good: {anomaly_pct:.2f}% anomalies")
                        else:
                            st.warning(f"Needs attention: {anomaly_pct:.2f}% anomalies")
                    
                    st.dataframe(anomalies_ml.head(15), use_container_width=True)
                else:
                    st.success("No ML-based anomalies detected")
            
            # Summary
            with anomaly_tab3:
                st.subheader("Anomaly Detection Summary")
                
                z_count = len(all_z_anomalies[0]) if all_z_anomalies else 0
                ml_count = len(anomalies_ml) if not anomalies_ml.empty else 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Z-Score Anomalies", z_count)
                
                with col2:
                    st.metric("ML Anomalies", ml_count)
                
                with col3:
                    st.metric("Total Flagged", z_count + ml_count)
                
                # Scatter plot showing anomalies vs normals
                if numeric_cols and len(numeric_cols) >= 2:
                    col1_name = numeric_cols[0]
                    col2_name = numeric_cols[1]
                    
                    plot_df = df[[col1_name, col2_name]].copy()
                    plot_df['Type'] = 'Normal'
                    if not anomalies_ml.empty:
                        plot_df.loc[anomalies_ml.index, 'Type'] = 'Anomalous'
                    
                    fig_scatter = px.scatter(
                        plot_df,
                        x=col1_name,
                        y=col2_name,
                        color='Type',
                        title=f"Anomaly Distribution: {col1_name} vs {col2_name}",
                        color_discrete_map={'Normal': '#3498db', 'Anomalous': '#e74c3c'}
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error in anomaly detection: {e}")

    # ============================================
    # SECTION 6: BUSINESS INSIGHTS
    # ============================================
    st.header("Step 6: Executive Insights")
    
    try:
        metrics = detect_metric_columns(df)
        kpis = calculate_basic_kpis(df, metrics) if metrics else {}
        trends = calculate_trends(df, metrics) if metrics else {}
        numeric_cols = list(metrics.keys()) if metrics else []
        anomalies_ml = detect_isolation_forest_outliers(df, numeric_cols) if numeric_cols else pd.DataFrame()
        segments = detect_important_segments(df, metrics if metrics else {})
        
        # Generate business insights
        business_insights = generate_business_insights(df, kpis, trends, anomalies_ml, segments)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Findings")
            st.markdown(business_insights)
        
        with col2:
            st.subheader("Recommendations")
            recommendations = generate_business_recommendations(kpis, trends, anomalies_ml, df, segments)
            
            if recommendations:
                for i, rec in enumerate(recommendations[:5], 1):
                    priority_color = "red" if rec['priority'] == "High" else "orange" if rec['priority'] == "Medium" else "green"
                    st.write(f"**[{rec['priority']} Priority {i}]**")
                    st.write(f"**Action:** {rec['action']}")
                    st.write(f"**Evidence:** {rec['evidence']}")
                    st.write(f"**Impact:** {rec['impact']}")
                    st.divider()
    
    except Exception as e:
        st.error(f"Error generating insights: {e}")

    # ============================================
    # SECTION 7: EXPORT REPORTS
    # ============================================
    st.header("Step 8: Export Reports")
    
    try:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("PDF Report")
            try:
                pdf_report = generate_pdf_report(df, kpis, trends, anomalies_ml, business_insights, recommendations)
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_report,
                    file_name="executive_report.pdf",
                    mime="application/pdf",
                    key="pdf_download"
                )
            except Exception as e:
                st.error(f"PDF error: {e}")
        
        with col2:
            st.subheader("KPIs (CSV)")
            try:
                csv_kpis = export_kpis_to_csv(kpis)
                st.download_button(
                    label="Download KPIs",
                    data=csv_kpis,
                    file_name="kpis.csv",
                    mime="text/csv",
                    key="kpi_csv"
                )
            except Exception as e:
                st.error(f"CSV error: {e}")
        
        with col3:
            st.subheader("Anomalies (CSV)")
            try:
                csv_anomalies = export_anomalies_to_csv(anomalies_ml)
                st.download_button(
                    label="Download Anomalies",
                    data=csv_anomalies,
                    file_name="anomalies.csv",
                    mime="text/csv",
                    key="anomaly_csv"
                )
            except Exception as e:
                st.error(f"CSV error: {e}")
    
    except Exception as e:
        st.error(f"Error in report generation: {e}")

else:
    st.info("Load data from the sidebar to get started")
    st.write("""
    AI Data Autopilot helps executives understand their data:
    - Quality assessment
    - KPI auto-detection
    - Anomaly detection (2 methods)
    - Business insights
    - Executive recommendations
    - Professional PDF reports
    """)