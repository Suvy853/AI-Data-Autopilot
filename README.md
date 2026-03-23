# AI DATA AUTOPILOT
A production-ready data analysis application that automatically cleans, analyzes, detects anomalies, and generates professional executive reports with AI-powered insights.

## Live Demo
Try the app now: https://ai-data-autopilot.streamlit.app/

*No installation needed - upload your CSV and start analyzing!*
<img width="1898" height="862" alt="image" src="https://github.com/user-attachments/assets/71a9f2dd-b728-46e4-9d28-89ebd568ad8e" />


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
*Z-Score (Statistical Method)*
**How it works:**

1. Measures how many standard deviations a value is from the mean
2. Formula: Z = (X - Mean) / Standard Deviation
3. Threshold: |Z-Score| > 3 indicates outlier (99.7% confidence)

**Pros:**

4. Simple and interpretable
5. Fast computation
6. Good for normally distributed data

**Cons:**

7. Assumes normal distribution
8. Sensitive to extreme outliers
9. Doesn't account for multivariate patterns

Best for: Single metric anomalies, quick outlier detection

*Isolation Forest (ML-Based Method)*
**How it works:**

1. Unsupervised ML algorithm that isolates anomalies
2. Builds random forests and isolates anomalies by path length
3. Anomalies require fewer splits to isolate

**Pros:**

4. Detects multivariate anomalies
5. No distribution assumptions
7. Works with high-dimensional data
8. Fast and scalable

**Cons:**

9. Less interpretable than Z-Score
10. Requires contamination parameter tuning

Best for: Complex patterns, multivariate anomalies, non-linear relationships


### Combined Approach
Using both methods together:

1. Validates findings across methods
2. Catches both simple and complex anomalies
3. Higher confidence in results
4. Better stakeholder trust
5. Comprehensive analysis



## Key Features Explained
*Auto-Detected KPIs*

The system automatically scans the dataset and identifies all numeric columns to generate meaningful Key Performance Indicators (KPIs). For every detected metric, it calculates multiple statistical measures such as the average, total, minimum, maximum, and standard deviation. In addition to basic statistics, the system also evaluates trends and growth rates to provide a clearer understanding of how each metric evolves over time. This allows users to quickly understand the most important performance indicators in their data without needing to manually define them.

*Auto-Detected Segments*

The platform also performs intelligent segment discovery by automatically identifying categorical columns in the dataset. Once these segments are detected, the system groups and counts the members within each category and calculates relevant performance metrics for them. It also displays the distribution percentages of each segment, helping users understand how their data is divided across different groups. All of this happens automatically, removing the need for any manual configuration.

*Business-Focused Insights*

Beyond data analysis, the system focuses on generating insights that are meaningful from a business perspective. It evaluates segment performance, highlights key drivers of growth, and detects potential risk areas within the data. The insights are presented in clear, executive-friendly language so they can be easily understood by both technical and non-technical stakeholders. Each recommendation is supported by data evidence, making the insights practical and actionable.

*Professional Visualizations*

To make the insights easier to interpret, the platform generates a range of professional visualizations. These include sortable anomaly tables that highlight issues based on severity, distribution pie charts that show how segments are divided, and KPI comparison bar charts for quick metric evaluation. The system also provides quality assessment metrics and interactive visualizations powered by Plotly, allowing users to explore the data dynamically and gain deeper insights.




## Technical Stack

The project is built using Python 3.8+, which serves as the core programming language for data processing, analysis, and machine learning tasks. For data manipulation and transformation, the system relies on pandas, while NumPy is used for efficient numerical computations and array operations. To perform anomaly detection and other machine learning tasks, the project uses scikit-learn, implementing algorithms such as Isolation Forest and Z-Score–based detection to identify unusual patterns within datasets.

For data visualization, the application uses Plotly to create interactive charts that allow users to explore insights directly within the web interface. In addition, Matplotlib is used to generate static visualizations, particularly for exporting charts in reports and documents.

The user interface is built with Streamlit, which powers the interactive web application. This allows users to upload datasets, run automated analyses, and explore results through a simple and intuitive interface without needing technical setup.

To generate downloadable reports, the system integrates ReportLab, which enables the creation of structured PDF reports containing insights, charts, and analysis summaries.

Finally, the project includes a custom-built data quality assessment engine that evaluates datasets for issues such as missing values, inconsistencies, and anomalies. This helps ensure that the insights generated by the system are based on reliable and well-structured data.





## Business Value

This project is designed to deliver value to multiple stakeholders by simplifying data analysis, improving decision-making, and supporting machine learning workflows.

For data analysis teams, the platform significantly reduces the time required for initial data exploration by automating key analytical tasks. This can save up to 70% of the time typically spent on exploratory analysis. The system also ensures a consistent methodology across different datasets, making it easier for teams to standardize their analytical processes. In addition, it generates professional, production-ready reports that clearly explain technical findings, helping teams communicate results more effectively.

For business stakeholders, the project translates complex data insights into clear, executive-friendly summaries written in plain language. Instead of presenting raw metrics alone, the system provides actionable recommendations supported by data evidence. It also highlights segment-level insights, allowing businesses to better understand customer groups, markets, or operational segments and design more targeted strategies. At the same time, the system identifies potential risks and unusual patterns, enabling stakeholders to make more informed and proactive decisions.

For machine learning engineers, the platform provides valuable insights that support model development and evaluation. It helps identify useful patterns that can inform feature engineering, while also establishing a data quality baseline before model training begins. The built-in anomaly detection capabilities reveal unusual behaviors in the data, and the results are presented in an interpretable way, making them easier to explain and validate during model development and deployment.














