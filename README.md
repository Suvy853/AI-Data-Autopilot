# AI Data Autopilot

An intelligent data analysis system that automatically cleans, analyzes, detects anomalies, and generates professional executive reports in minutes.

**[Try the Live Demo](https://ai-data-autopilot.streamlit.app/)**

*No installation needed. Upload your CSV and start analyzing!*



## Screenshots

### Home Page
Upload CSV files or use sample data to start analysis. The app guides you through 8 dashboard sections of analysis.
<img width="1916" height="862" alt="image" src="https://github.com/user-attachments/assets/8956a9cc-8298-4d42-84b6-c5cec69d68fa" />


### Data Overview Dashboard
Automated data quality assessment with real-time metrics showing record count, column analysis, quality score, and data size.

<img width="1919" height="873" alt="image" src="https://github.com/user-attachments/assets/5f93e93c-fcd1-407e-ab09-c8f1e9933630" />


## What This Does

Transform raw CSV data into actionable business insights automatically:

- Upload any CSV file (or use sample data)
- Analyze with automated data quality checks and KPI detection
- Detect anomalies using statistical and ML-based methods
- Generate professional executive PDF reports in seconds

The entire 7-step pipeline runs automatically. No configuration needed.



## Quick Start

### Option 1: Live Demo (No Setup)
1. Go to: https://ai-data-autopilot.streamlit.app/
2. Click "Upload CSV" or use sample data
3. Click "Run Analysis"
4. Download professional PDF report

### Option 2: Local Installation
```bash
# Clone the repository
git clone https://github.com/Suvy853/AI-Data-Autopilot.git
cd AI-Data-Autopilot

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Then open: `http://localhost:8501`



## How It Works

Your data flows through this intelligent 7-step pipeline:

### 1. Data Ingestion
Upload CSV → Automatic profiling → Initial validation

### 2. Data Quality Assessment
Scan for missing values, duplicates, data types → Quality score (0-100%)

### 3. Automated Cleaning
Fill missing values → Remove duplicates → Standardize formats

### 4. KPI Detection
Auto-identify metrics → Calculate statistics (avg, sum, min, max, std dev)

### 5. Anomaly Detection
- Z-Score Method: Statistical outlier detection
- Isolation Forest: ML-based pattern detection
- Combined: Validates findings across both methods

### 6. Business Insights
Segment analysis → Growth drivers → Risk assessment → Recommendations

### 7. Executive Report
Professional 6-7 page PDF with:
- Executive summary
- Data quality metrics
- KPI analysis with charts
- Segment breakdown
- Trend analysis
- Prioritized recommendations



## Key Features

### Auto-Detected KPIs
The system scans your dataset and automatically identifies all numeric columns. It calculates averages, totals, min/max values, standard deviation, and trend analysis - all without any manual configuration.

### Auto-Detected Segments
Automatically finds categorical columns and segments your data. Shows distribution percentages and key metrics per segment, helping you understand how your data divides across groups.

### Dual Anomaly Detection
- Z-Score: Fast, interpretable statistical method
- Isolation Forest: Advanced ML detection for complex patterns
- Combined approach: Higher confidence, fewer false positives

### Business-Focused Insights
Goes beyond numbers. Analyzes segment performance, identifies growth drivers, detects risks, and presents findings in executive-friendly language with data-backed recommendations.

### Professional PDF Reports
6-7 page reports with clean formatting, proper section breaks, KPI visualizations, and actionable recommendations. Print-ready and presentation-ready.




## Technical Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Data Processing | pandas, NumPy |
| Machine Learning | scikit-learn (Isolation Forest) |
| Visualization | Plotly, Matplotlib |
| Web Framework | Streamlit |
| PDF Generation | ReportLab |
| Deployment | Streamlit Cloud |
| Version Control | Git, GitHub |



## Business Impact

### For Data Teams
- 70% faster exploratory analysis
- Consistent methodology across datasets
- Professional executive-ready reports

### For Business Stakeholders
- Clear insights in plain language
- Actionable recommendations backed by data
- Segment-level analysis for targeted strategies

### For ML Engineers
- Data quality baseline before model training
- Pattern discovery for feature engineering
- Interpretable results for explainability



## Sample Output

### Input
Messy CSV with customer data:
- Missing values, duplicates, mixed formats
- 18,300 records, 9 columns
- Unnamed segments and unclear metrics

### Output (Professional PDF Report)
- Clean data summary with quality score
- 4 auto-detected KPIs with full statistics
- Segment breakdown with distribution charts
- 912 anomalies identified with severity levels
- 4 prioritized recommendations with evidence
- Executive readiness assessment

Complete analysis in 2 minutes. Professional 6-page report ready for stakeholders.



## Project Structure

```
ai-data-autopilot/
├── app.py                          # Main Streamlit app
├── src/
│   ├── data_loader.py             # CSV ingestion & validation
│   ├── kpi_engine.py              # KPI detection & calculation
│   ├── anomaly.py                 # Z-Score & Isolation Forest
│   ├── narrative_enhanced.py       # Business insights generation
│   └── report.py                  # PDF report generation
├── sample_data/
│   └── subscription_data.csv       # Example dataset
├── requirements.txt                # Dependencies
├── .gitignore
├── README.md
└── .devcontainer/                 # Dev container config
```



## What's Next

This is a complete, production-ready system. Potential enhancements:

- Dashboard for recurring analysis schedules
- Database integration for large datasets
- Custom segment and KPI configuration
- Multiple algorithm ensemble methods
- Real-time streaming data support



## Project Statistics

- Pipeline Stages: 7
- Anomaly Methods: 2 (Z-Score + Isolation Forest)
- Auto-Detection: KPIs, segments, quality issues
- Report Pages: 6-7
- Setup Time: < 2 minutes
- Analysis Time: < 2 minutes
- Manual Configuration: None required



## Key Learning Outcomes

This project demonstrates:

- Data Engineering: End-to-end pipeline design
- Data Analysis: Statistical analysis and KPI detection
- Machine Learning: Anomaly detection algorithms
- Software Design: Modular architecture, separation of concerns
- Web Development: Interactive UI with Streamlit
- DevOps: Git workflows, cloud deployment
- Communication: Executive reporting and business insights



## License

Open source - feel free to fork, modify, and use for your own projects.



## Links

- GitHub: https://github.com/Suvy853/AI-Data-Autopilot
- Live Demo: https://ai-data-autopilot.streamlit.app/



## Questions?

Check out the [GitHub Issues](https://github.com/Suvy853/AI-Data-Autopilot/issues) or review the code documentation in the `src/` folder.



Built with care for data teams that want insights, not spreadsheets.
