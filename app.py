import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_loader import load_csv, check_data_quality, clean_data
from src.kpi_engine import detect_metric_columns, calculate_basic_kpis, calculate_trends, analyze_by_segment
from src.anomaly import detect_statistical_outliers, detect_isolation_forest_outliers, find_category_anomalies
from src.narrative_enhanced import (detect_important_segments, find_segment_anomalies, 
                          generate_business_insights, generate_business_recommendations,
                          format_anomalies_for_display)
from src.report import generate_pdf_report, export_kpis_to_csv, export_anomalies_to_csv, export_recommendations_to_csv


# Page configuration
st.set_page_config(page_title="AI Data Autopilot", layout="wide")

# ============================================
# HEADER
# ============================================
st.title("AI Data Autopilot")
st.write("Intelligent data analysis: Upload → Clean → Analyze → Detect → Insights → Report")

# ============================================
# SIDEBAR - LOAD DATA FIRST
# ============================================
with st.sidebar:
    st.header("Load Data")
    
    use_sample = st.sidebar.checkbox("Use Sample Data?", value=True, key="use_sample_data")
    
    df = None
    df_original = None
    
    if use_sample:
        try:
            df_original = load_csv("sample_data/subscription_data.csv")
            quality_report = check_data_quality(df_original)
            st.sidebar.success("Loaded sample data")
            df = clean_data(df_original.copy(), quality_report)
        except FileNotFoundError:
            st.sidebar.error("Sample data not found")
    else:
        uploaded_file = st.sidebar.file_uploader("Choose CSV file", type="csv", key="csv_uploader")
        if uploaded_file is not None:
            try:
                df_original = pd.read_csv(uploaded_file)
                quality_report = check_data_quality(df_original)
                st.sidebar.success(f"Loaded {uploaded_file.name}")
                df = clean_data(df_original.copy(), quality_report)
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    
    # ============================================
    # SIDEBAR - ARCHITECTURE PIPELINE
    # ============================================
    st.sidebar.markdown("---")
    st.sidebar.header("System Pipeline")
    st.sidebar.markdown("""
    **1. Data Ingestion**
    Upload or sample data
    
    **2. Quality Assessment**
    Check for issues
    
    **3. Auto Cleaning**
    Fill, remove duplicates
    
    **4. Metric Detection**
    Find KPIs, segments
    
    **5. Anomaly Detection**
    Z-Score + Isolation Forest
    
    **6. Business Insights**
    Segment analysis, growth drivers
    
    **7. AI Recommendations**
    Claude-powered actions
    
    **8. PDF Reports**
    Executive-ready documents
    """)

# ============================================
# MAIN CONTENT
# ============================================

if df is not None and df_original is not None:
    
    # ============================================
    # DATA OVERVIEW
    # ============================================
    st.subheader(" DATA OVERVIEW")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", f"{len(df):,}")
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        quality_score = check_data_quality(df)['quality_score']
        st.metric("Quality Score", f"{quality_score:.1f}%")
    with col4:
        st.metric("File Size", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # ============================================
    # DATA CLEANING
    # ============================================
    st.subheader("DATA CLEANING SUMMARY")
    
    tab1, tab2, tab3 = st.tabs(["Cleaning Summary", "Before Cleaning", "After Cleaning"])
    
    with tab1:
        st.write("### Data Quality Improvement")
        
        original_blanks = df_original.isnull().sum().sum()
        cleaned_blanks = df.isnull().sum().sum()
        blanks_removed = original_blanks - cleaned_blanks
        
        original_duplicates = len(df_original) - len(df_original.drop_duplicates())
        cleaned_duplicates = len(df) - len(df.drop_duplicates())
        duplicates_removed = original_duplicates - cleaned_duplicates
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Blank Cells Removed", f"{blanks_removed:,}", 
                     delta=f"-{blanks_removed:,}" if blanks_removed > 0 else "Clean")
        with col2:
            st.metric("Duplicates Removed", f"{duplicates_removed:,}",
                     delta=f"-{duplicates_removed:,}" if duplicates_removed > 0 else "Clean")
        with col3:
            quality_before = check_data_quality(df_original)['quality_score']
            quality_after = check_data_quality(df)['quality_score']
            quality_improvement = quality_after - quality_before
            st.metric("Quality Improvement", f"{quality_after:.1f}%",
                     delta=f"+{quality_improvement:.1f}%")
        with col4:
            row_retention = (len(df) / len(df_original)) * 100
            st.metric("Data Retained", f"{row_retention:.1f}%")
    
    with tab2:
        st.write("### Original Data (Before Cleaning)")
        st.dataframe(df_original.head(10), use_container_width=True)
    
    with tab3:
        st.write("### Cleaned Data (After Cleaning)")
        st.dataframe(df.head(10), use_container_width=True)

    # ============================================
    # KPI ANALYSIS
    # ============================================
    st.subheader("KEY PERFORMANCE INDICATORS (KPIs) ANALYSIS")
    
    try:
        metrics = detect_metric_columns(df)
        
        if metrics:
            kpis = calculate_basic_kpis(df, metrics)
            
            st.write("### Auto-Detected Metrics (KPIs)")
            st.write(f"Found {len(kpis)} numeric columns for analysis")
            
            kpi_col1, kpi_col2 = st.columns(2)
            
            with kpi_col1:
                st.write("### KPI Summary Table")
                kpi_df = pd.DataFrame(kpis).T[['average', 'sum', 'min', 'max']]
                st.dataframe(kpi_df, use_container_width=True)
            
            with kpi_col2:
                st.write("### KPI Comparison")
                kpi_averages = {col: values['average'] for col, values in kpis.items()}
                fig_bar = px.bar(x=list(kpi_averages.keys()), y=list(kpi_averages.values()),
                                labels={'x': 'Metric', 'y': 'Average Value'},
                                title="Average by Metric", color_continuous_scale='Blues')
                fig_bar.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No numeric columns found for KPI analysis")
    except Exception as e:
        st.error(f"Error in KPI analysis: {e}")

    # ============================================
    # SEGMENT ANALYSIS
    # ============================================
    st.subheader("SEGMENT ANALYSIS")
    
    try:
        segments = detect_important_segments(df, metrics if metrics else {})
        
        if segments:
            st.write("### Key Segments Detected")
            
            for segment_col, segment_data in segments.items():
                st.write(f"#### By {segment_col}")
                
                segment_display = []
                for seg_name, seg_info in segment_data.items():
                    segment_display.append({
                        'Segment': seg_name,
                        'Count': seg_info['count'],
                        'Percentage': f"{seg_info['percentage']:.1f}%"
                    })
                
                segment_df = pd.DataFrame(segment_display)
                st.dataframe(segment_df, use_container_width=True)
                
                fig_pie = px.pie(values=[s['Count'] for s in segment_display],
                               names=[s['Segment'] for s in segment_display],
                               title=f"Distribution by {segment_col}")
                st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No clear segments detected in this dataset")
    except Exception as e:
        st.error(f"Error in segment analysis: {e}")

    # ============================================
    # ANOMALY DETECTION
    # ============================================
    st.subheader("ANOMALY DETECTION")
    
    st.write("""
    ### Anomaly Detection Methods Explained
    
    **Method 1: Z-Score (Statistical)**
    - Measures how far from average (in standard deviations)
    - Threshold: >3 is outlier (99.7% confidence)
    - Best for: Single metric anomalies, normally distributed data
    
    **Method 2: Isolation Forest (Machine Learning)**
    - Isolates anomalies as patterns different from normal
    - No assumptions about data distribution
    - Best for: Complex, multivariate anomalies
    """)
    
    try:
        numeric_cols = list(metrics.keys()) if metrics else []
        
        if numeric_cols:
            anomaly_tab1, anomaly_tab2, anomaly_tab3 = st.tabs(
                ["Statistical (Z-Score)", "ML-Based (Isolation Forest)", "Summary"]
            )
            
            # Z-Score Anomalies
            with anomaly_tab1:
                st.write("### Statistical Outliers (Z-Score Method)")
                
                all_z_anomalies = []
                for col in numeric_cols[:3]:
                    outliers = detect_statistical_outliers(df, col)
                    if len(outliers) > 0:
                        all_z_anomalies.append(outliers)
                
                if all_z_anomalies:
                    z_anomalies = pd.concat(all_z_anomalies, ignore_index=True)
                    st.write(f"Found {len(z_anomalies)} statistical outliers")
                    
                    z_display = z_anomalies.copy()
                    if 'z_score' in z_display.columns:
                        z_display['Severity'] = z_display['z_score'].apply(
                            lambda x: 'Critical' if abs(x) > 4 else 'High' if abs(x) > 3 else 'Medium'
                        )
                    
                    st.dataframe(z_display.head(20), use_container_width=True)
                else:
                    st.success("No statistical outliers detected")
            
            # ML Anomalies
            with anomaly_tab2:
                st.write("### ML-Based Anomalies (Isolation Forest)")
                
                anomalies_ml = detect_isolation_forest_outliers(df, numeric_cols)
                
                if len(anomalies_ml) > 0:
                    st.warning(f"Found {len(anomalies_ml)} anomalous records")
                    
                    anomaly_stats = {
                        'Normal Records': len(df) - len(anomalies_ml),
                        'Anomalous Records': len(anomalies_ml)
                    }
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_pie = px.pie(values=list(anomaly_stats.values()),
                                       names=list(anomaly_stats.keys()),
                                       title="Data Distribution")
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col2:
                        anomaly_pct = (len(anomalies_ml) / len(df) * 100)
                        if anomaly_pct < 2:
                            st.success(f"Excellent: Only {anomaly_pct:.2f}% anomalies")
                        elif anomaly_pct < 5:
                            st.info(f"Good: {anomaly_pct:.2f}% anomalies")
                        else:
                            st.warning(f"Needs attention: {anomaly_pct:.2f}% anomalies")
                    
                    st.write("### Anomalous Records (sortable)")
                    anomaly_display = anomalies_ml.copy()
                    st.dataframe(anomaly_display.head(20), use_container_width=True)
                else:
                    st.success("No ML-based anomalies detected")
            
            # Summary
            with anomaly_tab3:
                st.write("### Anomaly Detection Summary")
                
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                
                with summary_col1:
                    z_count = len(all_z_anomalies[0]) if all_z_anomalies else 0
                    st.metric("Z-Score Anomalies", z_count)
                
                with summary_col2:
                    ml_count = len(anomalies_ml)
                    st.metric("ML Anomalies", ml_count)
                
                with summary_col3:
                    total_anomalies = z_count + ml_count
                    st.metric("Total Flagged", total_anomalies)
                
                st.write("### Method Comparison")
                comparison = pd.DataFrame({
                    'Method': ['Z-Score', 'Isolation Forest'],
                    'Anomalies Found': [z_count, ml_count],
                    'Type': ['Statistical', 'ML-Based'],
                    'Best For': ['Single metrics', 'Complex patterns']
                })
                st.dataframe(comparison, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error in anomaly detection: {e}")

    # ============================================
    # BUSINESS INSIGHTS
    # ============================================
    st.subheader("BUSINESS INSIGHTS & AI RECOMMENDATIONS")
    
    try:
        metrics = detect_metric_columns(df)
        kpis = calculate_basic_kpis(df, metrics) if metrics else {}
        trends = calculate_trends(df, metrics) if metrics else {}
        numeric_cols = list(metrics.keys()) if metrics else []
        anomalies_ml = detect_isolation_forest_outliers(df, numeric_cols) if numeric_cols else pd.DataFrame()
        segments = detect_important_segments(df, metrics if metrics else {})
        
        business_insights = generate_business_insights(df, kpis, trends, anomalies_ml, segments)
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.write("### Business Analysis")
            st.markdown(business_insights)
        
        with insight_col2:
            st.write("### Recommendations")
            recommendations = generate_business_recommendations(kpis, trends, anomalies_ml, df, segments)
            
            if recommendations:
                for i, rec in enumerate(recommendations[:5], 1):
                    color = '🔴' if rec['priority'] == 'High' else '🟡' if rec['priority'] == 'Medium' else '🟢'
                    st.write(f"**{color} {i}. {rec['action']}**")
                    st.write(f"Evidence: {rec['evidence']}")
                    st.write(f"Impact: {rec['impact']}")
                    st.write(f"Metric: {rec['metric']}")
                    st.write("---")
        
        if recommendations:
            st.write("### All Recommendations (Sortable)")
            rec_display = pd.DataFrame([
                {
                    'Priority': rec['priority'],
                    'Action': rec['action'],
                    'Evidence': rec['evidence'],
                    'Impact': rec['impact'],
                    'Segment': rec.get('segment', 'General')
                }
                for rec in recommendations
            ])
            st.dataframe(rec_display, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error generating insights: {e}")

    # ============================================
    # REPORT GENERATION
    # ============================================
    st.subheader("DOWNLOADABLE REPORTS & DATA EXPORTS")
    
    try:
        metrics = detect_metric_columns(df)
        kpis = calculate_basic_kpis(df, metrics) if metrics else {}
        trends = calculate_trends(df, metrics) if metrics else {}
        numeric_cols = list(metrics.keys()) if metrics else []
        anomalies_ml = detect_isolation_forest_outliers(df, numeric_cols) if numeric_cols else pd.DataFrame()
        narrative = generate_business_insights(df, kpis, trends, anomalies_ml, 
                                             detect_important_segments(df, metrics if metrics else {}))
        recommendations = generate_business_recommendations(kpis, trends, anomalies_ml, df,
                                                          detect_important_segments(df, metrics if metrics else {}))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### PDF Executive Report")
            st.write("Professional report with charts and recommendations")
            
            pdf_report = generate_pdf_report(df, kpis, trends, anomalies_ml, narrative, recommendations)
            
            st.download_button(
                label="Download PDF Report",
                data=pdf_report,
                file_name="executive_report.pdf",
                mime="application/pdf",
                key="pdf_download"
            )
        
        with col2:
            st.write("### CSV Data Exports")
            
            export_option = st.selectbox("Select export type",
                ["KPIs (CSV)", "Anomalies (CSV)", "Recommendations (CSV)"],
                key="export_selectbox")
            
            if export_option == "KPIs (CSV)":
                csv_data = export_kpis_to_csv(kpis)
                st.download_button("Download KPIs", csv_data, "kpis.csv", "text/csv", key="kpi_csv")
            elif export_option == "Anomalies (CSV)":
                csv_data = export_anomalies_to_csv(anomalies_ml)
                st.download_button("Download Anomalies", csv_data, "anomalies.csv", "text/csv", key="anomaly_csv")
            else:
                csv_data = export_recommendations_to_csv(recommendations)
                st.download_button("Download Recommendations", csv_data, "recommendations.csv", "text/csv", key="rec_csv")
    
    except Exception as e:
        st.error(f"Error generating reports: {e}")



else:
    st.info("Load data to get started (check 'Use Sample Data?' or upload CSV)")