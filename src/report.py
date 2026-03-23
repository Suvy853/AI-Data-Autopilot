import pandas as pd
import io
import tempfile
import re
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import plotly.express as px


def generate_pdf_report(df, kpis, trends, anomalies, insights, recommendations):
    """
    Generate professional executive report with properly formatted Executive Summary.
    NO blank pages, proper section formatting.
    """
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # ============================================
    # STYLE DEFINITIONS
    # ============================================
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontName="Helvetica-Bold",
        fontSize=28,
        leading=34,
        spaceAfter=12,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        name="SubtitleStyle",
        fontName="Helvetica",
        fontSize=14,
        leading=18,
        spaceAfter=6,
        textColor=colors.HexColor('#333333'),
        alignment=1
    )
    
    date_style = ParagraphStyle(
        name="DateStyle",
        fontName="Helvetica",
        fontSize=11,
        leading=13,
        spaceAfter=24,
        textColor=colors.HexColor('#666666'),
        alignment=1
    )
    
    heading1_style = ParagraphStyle(
        name="Heading1Style",
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=19,
        spaceAfter=12,
        textColor=colors.HexColor('#1a1a1a'),
        spaceBefore=12
    )
    
    heading2_style = ParagraphStyle(
        name="Heading2Style",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        spaceAfter=10,
        textColor=colors.HexColor('#333333'),
        spaceBefore=10
    )
    
    heading3_style = ParagraphStyle(
        name="Heading3Style",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        spaceAfter=6,
        textColor=colors.HexColor('#444444'),
        spaceBefore=8
    )
    
    body_style = ParagraphStyle(
        name="BodyStyle",
        fontName="Helvetica",
        fontSize=10,
        leading=13,
        spaceAfter=8,
        alignment=4
    )
    
    elements = []
    
    # ============================================
    # TITLE PAGE (PAGE 1)
    # ============================================
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("DATA ANALYSIS REPORT", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Executive Summary and Data Quality Assessment", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    current_date = datetime.now().strftime("%B %d, %Y")
    elements.append(Paragraph(f"Report Date: {current_date}", date_style))
    elements.append(Spacer(1, 1.5*inch))
    
    intro_text = "This report provides a comprehensive analysis of your dataset, including data quality assessment, key performance indicators, segment analysis, and actionable recommendations."
    elements.append(Paragraph(intro_text, body_style))
    
    elements.append(PageBreak())
    
    # ============================================
    # PAGE 2: EXECUTIVE SUMMARY - PROPERLY FORMATTED
    # ============================================
    elements.append(Paragraph("Executive Summary", heading1_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Parse insights into proper sections
    section_headers = [
        "Data Quality Assessment",
        "Key Performance Indicators",
        "Segment Analysis",
        "Growth and Trend Analysis",
        "Data Anomalies and Outliers",
        "Executive Readiness Summary"
    ]
    
    # Split insights by double newlines
    parts = insights.split("\n\n")
    
    current_text = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Check if this part is a section header
        if part in section_headers:
            # Add previous accumulated text if any
            if current_text.strip():
                elements.append(Paragraph(current_text.strip(), body_style))
                elements.append(Spacer(1, 0.08*inch))
            
            # Add new section header
            elements.append(Spacer(1, 0.05*inch))
            elements.append(Paragraph(part, heading3_style))
            elements.append(Spacer(1, 0.05*inch))
            current_text = ""
        else:
            # Accumulate body text
            current_text += part + " "
    
    # Add final accumulated text
    if current_text.strip():
        elements.append(Paragraph(current_text.strip(), body_style))
    
    elements.append(Spacer(1, 0.15*inch))
    
    # ============================================
    # PAGE 2 CONTINUED: DATASET OVERVIEW
    # ============================================
    elements.append(Paragraph("Dataset Overview", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    quality_score = 100 - (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    
    overview_intro = f"The analyzed dataset contains {len(df):,} records across {len(df.columns)} columns, representing {df.memory_usage(deep=True).sum() / (1024*1024):.2f} megabytes of data. The dataset has been assessed for quality, cleaned, and prepared for analysis. Data quality score is {quality_score:.1f} percent."
    
    elements.append(Paragraph(overview_intro, body_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Dataset metrics table
    overview_data = [
        ["Metric", "Value"],
        ["Total Records", f"{len(df):,}"],
        ["Total Columns", str(len(df.columns))],
        ["Data Size", f"{df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB"],
        ["Blank Cells", f"{df.isnull().sum().sum():,}"],
        ["Duplicate Rows", f"{len(df) - len(df.drop_duplicates())}"],
    ]
    
    overview_table = Table(overview_data, colWidths=[2.5*inch, 2.5*inch])
    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#333333')),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
        ("GRID", (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
        ("ROWHEIGHT", (0, 0), (-1, -1), 0.3*inch),
    ]))
    
    elements.append(overview_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Data quality assessment
    elements.append(Paragraph("Data Quality Assessment", heading2_style))
    elements.append(Spacer(1, 0.08*inch))
    
    if quality_score >= 95:
        quality_text = f"The dataset exhibits excellent quality with a score of {quality_score:.1f} percent. Data is reliable and ready for comprehensive analysis."
    elif quality_score >= 80:
        quality_text = f"The dataset quality is good with a score of {quality_score:.1f} percent. Data has been cleaned and is suitable for analysis."
    else:
        quality_text = f"The dataset requires attention with a quality score of {quality_score:.1f} percent. Data inconsistencies were identified and addressed."
    
    elements.append(Paragraph(quality_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # PAGE 3: KEY PERFORMANCE INDICATORS
    # ============================================
    elements.append(PageBreak())
    elements.append(Paragraph("Key Performance Indicators", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    if kpis:
        kpi_intro = f"The analysis identified {len(kpis)} key performance indicators in your dataset. Below is a summary of primary metrics and their statistical measures."
        elements.append(Paragraph(kpi_intro, body_style))
        elements.append(Spacer(1, 0.15*inch))
        
        # KPI Table
        kpi_data = [["Metric", "Average", "Minimum", "Maximum"]]
        
        for metric, values in list(kpis.items())[:10]:
            metric_name = metric.replace("_", " ").title()[:25]
            kpi_data.append([
                metric_name,
                f"{values.get('average', 0):,.0f}",
                f"{values.get('min', 0):,.0f}",
                f"{values.get('max', 0):,.0f}"
            ])
        
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        kpi_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#333333')),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ("GRID", (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ("ROWHEIGHT", (0, 0), (-1, -1), 0.28*inch),
        ]))
        
        elements.append(kpi_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # PAGE 4: SEGMENT AND TREND ANALYSIS
    # ============================================
    elements.append(PageBreak())
    elements.append(Paragraph("Segment Analysis", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    segment_text = "Customer segments have been automatically identified from categorical variables in the dataset. Understanding segment distribution helps target strategies and allocate resources effectively."
    elements.append(Paragraph(segment_text, body_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Trend Analysis
    elements.append(Paragraph("Trend Analysis", heading2_style))
    elements.append(Spacer(1, 0.1*inch))
    
    if trends:
        trend_intro = "Metric performance over time reveals important business patterns and directional changes."
        elements.append(Paragraph(trend_intro, body_style))
        elements.append(Spacer(1, 0.12*inch))
        
        trend_data = [["Metric", "Total Growth", "Monthly Growth", "Status"]]
        
        for metric, trend_vals in list(trends.items())[:8]:
            growth = trend_vals.get('total_growth_percent', 0)
            monthly_growth = trend_vals.get('avg_monthly_growth_percent', 0)
            
            if growth > 10:
                status = "Growing"
            elif growth < -10:
                status = "Declining"
            else:
                status = "Stable"
            
            metric_name = metric.replace("_", " ").title()[:20]
            trend_data.append([
                metric_name,
                f"{growth:+.1f}%",
                f"{monthly_growth:+.1f}%",
                status
            ])
        
        trend_table = Table(trend_data, colWidths=[1.3*inch, 1.3*inch, 1.3*inch, 1.1*inch])
        trend_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor('#333333')),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor('#f5f5f5')),
            ("GRID", (0, 0), (-1, -1), 1, colors.HexColor('#cccccc')),
            ("ROWHEIGHT", (0, 0), (-1, -1), 0.28*inch),
        ]))
        
        elements.append(trend_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Data Quality and Anomalies
    elements.append(Paragraph("Data Quality and Anomalies", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    if anomalies is not None and not anomalies.empty:
        anomaly_pct = (len(anomalies) / len(df)) * 100
        
        if anomaly_pct < 1:
            anomaly_text = f"Anomaly detection identified {len(anomalies)} anomalous records ({anomaly_pct:.2f} percent of dataset). The low anomaly rate indicates high data reliability and consistency."
        elif anomaly_pct < 5:
            anomaly_text = f"Anomaly detection identified {len(anomalies)} anomalous records ({anomaly_pct:.2f} percent of dataset). The moderate anomaly rate is acceptable for most applications. These records deviate from expected patterns and may warrant review."
        else:
            anomaly_text = f"Anomaly detection identified {len(anomalies)} anomalous records ({anomaly_pct:.2f} percent of dataset). The elevated anomaly rate suggests data quality issues that should be addressed."
        
        elements.append(Paragraph(anomaly_text, body_style))
    else:
        elements.append(Paragraph("No significant anomalies were detected. The dataset appears consistent with expected patterns.", body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # PAGE 5: RECOMMENDATIONS
    # ============================================
    elements.append(PageBreak())
    elements.append(Paragraph("Recommendations", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    if recommendations:
        for i, rec in enumerate(recommendations[:8], 1):
            priority = rec.get('priority', 'Medium')
            action = rec.get('action', 'N/A')
            evidence = rec.get('evidence', 'N/A')
            impact = rec.get('impact', 'N/A')
            metric = rec.get('metric', 'General')
            
            rec_header = f"Recommendation {i} ({priority} Priority)"
            elements.append(Paragraph(rec_header, heading2_style))
            elements.append(Spacer(1, 0.08*inch))
            
            rec_text = f"Action: {action}\n\nEvidence: {evidence}\n\nBusiness Impact: {impact}\n\nAssociated Metric: {metric}"
            elements.append(Paragraph(rec_text, body_style))
            elements.append(Spacer(1, 0.12*inch))
    else:
        elements.append(Paragraph("Data is ready for detailed analysis. No critical issues identified.", body_style))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # ============================================
    # PAGE 6: CONCLUSION
    # ============================================
    elements.append(PageBreak())
    elements.append(Paragraph("Conclusion", heading1_style))
    elements.append(Spacer(1, 0.1*inch))
    
    conclusion_text = "This data quality assessment provides a foundation for informed decision-making. The identified key metrics, segments, and trends establish baseline understanding of your data. We recommend proceeding with detailed analytics in alignment with the recommendations outlined above. For further analysis or clarification, please consult with your analytics team."
    
    elements.append(Paragraph(conclusion_text, body_style))
    elements.append(Spacer(1, 0.5*inch))
    
    footer_text = f"Report generated on {current_date} by AI Data Autopilot. This report is confidential and intended for authorized recipients only."
    elements.append(Paragraph(footer_text, body_style))
    
    # ============================================
    # BUILD PDF
    # ============================================
    try:
        doc.build(elements)
    except Exception as e:
        print(f"PDF build error: {e}")
    
    buffer.seek(0)
    return buffer


def export_kpis_to_csv(kpis):
    """Export KPIs to CSV format."""
    if not kpis:
        return ""
    
    df = pd.DataFrame(kpis).T
    return df.to_csv(index=True)


def export_anomalies_to_csv(anomalies):
    """Export anomalies to CSV format."""
    if anomalies is None or anomalies.empty:
        return ""
    
    return anomalies.to_csv(index=False)


def export_recommendations_to_csv(recommendations):
    """Export recommendations to CSV format."""
    if not recommendations:
        return ""
    
    df = pd.DataFrame(recommendations)
    return df.to_csv(index=False)