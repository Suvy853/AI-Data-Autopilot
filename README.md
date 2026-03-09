## System Architecture

### Pipeline Workflow

┌─────────────────────────────────────────────────────────────────┐
│ 1. DATA INGESTION                                               │
│    • Upload CSV file or use sample data                         │
│    • Load data into pandas DataFrame                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. DATA QUALITY ASSESSMENT                                      │
│    • Check for missing values, duplicates, data types           │
│    • Calculate quality score (0-100%)                           │
│    • Identify data issues                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. AUTOMATED DATA CLEANING                                      │
│    • Fill missing values (median for numeric, mode for text)    │
│    • Remove duplicates                                          │
│    • Standardize column names and values                        │
│    • Handle data type conversions                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. METRIC DETECTION & KPI ANALYSIS                              │
│    • Auto-detect numeric columns (metrics)                      │
│    • Calculate: average, sum, min, max, std dev                 │
│    • Identify trends (if date column exists)                    │
│    • Detect key segments (categories, groups)                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. ANOMALY DETECTION (2 Methods)                                │
│    • Statistical: Z-Score (3+ standard deviations)              │
│    • ML-Based: Isolation Forest (unsupervised learning)         │
│    • Result: Detailed anomaly scores and severity levels        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. BUSINESS INSIGHT GENERATION                                  │
│    • Analyze segment performance                                │
│    • Identify growth drivers and problem areas                  │
│    • Generate context-aware recommendations                     │
│    • Assess business impact of anomalies                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. AI-POWERED RECOMMENDATIONS                                   │
│    • Claude API generates narrative analysis                    │
│    • Priority-based recommendations (High/Medium/Low)           │
│    • Evidence and business impact for each action               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. PROFESSIONAL REPORT GENERATION                               │
│    • PDF Executive Report with:                                 │
│      - Executive Summary (AI-generated)                         │
│      - Data Overview & Quality Metrics                          │
│      - KPI Analysis with Visualizations                         │
│      - Anomaly Detection Analysis                               │
│      - Trend Analysis with Growth Charts                        │
│      - Prioritized Recommendations                              │
│      - Segment Performance Breakdown                            │
└────────────────────────┬────────────────────────────────────────┘

