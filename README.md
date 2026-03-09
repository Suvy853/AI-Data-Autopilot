# AI DATA AUTOPILOT
A production-ready data analysis application that automatically cleans, analyzes, detects anomalies, and generates professional executive reports with AI-powered insights.


## Project Overview
AI Data Autopilot is an intelligent data analysis system that transforms raw CSV data into actionable business insights in minutes. It combines automated data engineering, statistical analysis, machine learning anomaly detection, and AI-generated business recommendations.

*Key Features:*
1. Automatic: Auto-detects data quality issues, KPIs, and anomalies
2. Intelligent: Uses ML for sophisticated anomaly detection
3. Business-Focused: Generates segment-based insights, not just technical stats
4. Professional: Produces executive-ready PDF reports with charts
5. Comprehensive: 7-step pipeline from data ingestion to insights

## System Architecture

7-Step Pipeline
Your data flows through this intelligent pipeline:

*Step 1: Data Ingestion*

1. Upload CSV file or use sample data
2. Load data into pandas DataFrame
3. Initial validation and profiling

*Step 2: Data Quality Assessment*

4. Check for missing values and duplicates
5. Calculate quality score (0-100%)
6. Identify data issues and anomalies
7. Provide quality metrics

*Step 3: Automated Data Cleaning*

8. Fill missing values (median for numeric, mode for text)
9. Remove duplicate records
10. Standardize column names and values
11. Handle data type conversions

*Step 4: Metric Detection & KPI Analysis*

12. Auto-detect numeric columns (metrics)
13. Calculate: average, sum, min, max, std dev
14. Identify trends (if date column exists)
15. Detect key segments (categories, groups)

*Step 5: Anomaly Detection*

16. Z-Score (Statistical): Identifies outliers based on standard deviations
17. Isolation Forest (ML-Based): Unsupervised learning for complex patterns
18. Result: Detailed anomaly scores and severity levels
19. Sortable tables with severity classification

*Step 6: Business Insight Generation*

20. Analyze segment performance
21. Identify growth drivers and problem areas
22. Generate context-aware recommendations
23.Assess business impact of anomalies

*Step 7: Professional Report Generation*

1. PDF Executive Report with:

   Executive Summary,Data Overview & Quality Metrics,KPI Analysis with Visualizations, Anomaly Detection Analysis,Trend Analysis with Growth Charts,Prioritized Recommendations,Segment Performance Breakdown


## Anomaly Detection Methods
Z-Score (Statistical Method)
How it works:

Measures how many standard deviations a value is from the mean
Formula: Z = (X - Mean) / Standard Deviation
Threshold: |Z-Score| > 3 indicates outlier (99.7% confidence)

Pros:

Simple and interpretable
Fast computation
Good for normally distributed data

Cons:

Assumes normal distribution
Sensitive to extreme outliers
Doesn't account for multivariate patterns

Best for: Single metric anomalies, quick outlier detection


