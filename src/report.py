import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from typing import Dict, List
from datetime import datetime
import io


def generate_kpi_chart(kpis: Dict) -> str:
    """
    Generate KPI bar chart as image.
    Returns base64 encoded image.
    """
    if not kpis:
        return None
    
    try:
        kpi_averages = {col: values['average'] for col, values in list(kpis.items())[:5]}
        
        plt.figure(figsize=(10, 5))
        plt.bar(range(len(kpi_averages)), list(kpi_averages.values()), color='#3498db')
        plt.xlabel('Metrics', fontsize=12, fontweight='bold')
        plt.ylabel('Average Value', fontsize=12, fontweight='bold')
        plt.title('Key Performance Indicators', fontsize=14, fontweight='bold')
        plt.xticks(range(len(kpi_averages)), list(kpi_averages.keys()), rotation=45, ha='right')
        plt.tight_layout()
        
        # Save to bytes
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
        img_bytes.seek(0)
        plt.close()
        
        return img_bytes
    except Exception as e:
        plt.close()
        return None


def generate_anomaly_chart(anomalies: pd.DataFrame, total_records: int) -> str:
    """
    Generate anomaly pie chart as image.
    """
    try:
        normal = total_records - len(anomalies)
        anomalous = len(anomalies)
        
        plt.figure(figsize=(8, 6))
        sizes = [normal, anomalous]
        labels = [f'Normal Records\n({normal:,})', f'Anomalous Records\n({anomalous:,})']
        colors_pie = ['#2ecc71', '#e74c3c']
        
        plt.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
        plt.title('Data Quality Distribution', fontsize=14, fontweight='bold')
        plt.axis('equal')
        plt.tight_layout()
        
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
        img_bytes.seek(0)
        plt.close()
        
        return img_bytes
    except Exception as e:
        plt.close()
        return None


def generate_trend_chart(trends: Dict) -> str:
    """
    Generate trend growth chart as image.
    """
    if not trends:
        return None
    
    try:
        metrics = list(trends.keys())[:5]
        growth_rates = [trends[m]['total_growth_percent'] for m in metrics]
        
        plt.figure(figsize=(10, 5))
        colors_list = ['#27ae60' if x > 0 else '#e74c3c' for x in growth_rates]
        plt.bar(range(len(metrics)), growth_rates, color=colors_list)
        plt.xlabel('Metrics', fontsize=12, fontweight='bold')
        plt.ylabel('Growth Percentage (%)', fontsize=12, fontweight='bold')
        plt.title('Metric Growth Analysis', fontsize=14, fontweight='bold')
        plt.xticks(range(len(metrics)), metrics, rotation=45, ha='right')
        plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format='png', dpi=100, bbox_inches='tight')
        img_bytes.seek(0)
        plt.close()
        
        return img_bytes
    except Exception as e:
        plt.close()
        return None


def generate_pdf_report(df: pd.DataFrame, kpis: Dict, trends: Dict, anomalies: pd.DataFrame, 
                       narrative: str, recommendations: List[Dict]) -> bytes:
    """
    Generate professional PDF executive report.
    Returns PDF as bytes.
    """
    
    # Create PDF
    pdf_bytes = io.BytesIO()
    doc = SimpleDocTemplate(pdf_bytes, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    # Story for PDF
    story = []
    
    # Title Page
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("DATA ANALYSIS REPORT", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary Section
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    story.append(Paragraph(narrative, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Data Overview
    story.append(Paragraph("DATA OVERVIEW", heading_style))
    
    overview_data = [
        ['Metric', 'Value'],
        ['Total Records', f"{len(df):,}"],
        ['Total Columns', f"{len(df.columns)}"],
        ['File Size', f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"],
        ['Quality Score', f"{((len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns)) * 100):.1f}%"],
        ['Anomalies Detected', f"{len(anomalies):,}"]
    ]
    
    overview_table = Table(overview_data, colWidths=[3*inch, 2*inch])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    story.append(overview_table)
    story.append(Spacer(1, 0.3*inch))
    
    # KPI Analysis
    story.append(Paragraph("KEY PERFORMANCE INDICATORS", heading_style))
    
    if kpis:
        # Add KPI chart
        kpi_chart = generate_kpi_chart(kpis)
        if kpi_chart:
            try:
                img_kpi = Image(kpi_chart, width=5.5*inch, height=2.75*inch)
                story.append(img_kpi)
                story.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # KPI Table
        kpi_table_data = [['Metric', 'Average', 'Sum', 'Min', 'Max', 'Std Dev']]
        for metric_name, metric_values in list(kpis.items())[:5]:
            kpi_table_data.append([
                metric_name[:15],
                f"{metric_values.get('average', 0):,.2f}",
                f"{metric_values.get('sum', 0):,.0f}",
                f"{metric_values.get('min', 0):,.2f}",
                f"{metric_values.get('max', 0):,.2f}",
                f"{metric_values.get('std_dev', 0):,.2f}"
            ])
        
        kpi_table = Table(kpi_table_data, colWidths=[1.2*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        
        story.append(kpi_table)
    
    story.append(PageBreak())
    
    # Anomaly Detection
    story.append(Paragraph("ANOMALY DETECTION ANALYSIS", heading_style))
    
    anomaly_chart = generate_anomaly_chart(anomalies, len(df))
    if anomaly_chart:
        try:
            img_anomaly = Image(anomaly_chart, width=4*inch, height=3*inch)
            story.append(img_anomaly)
            story.append(Spacer(1, 0.2*inch))
        except:
            pass
    
    # Anomaly summary
    anomaly_pct = (len(anomalies) / len(df) * 100) if len(df) > 0 else 0
    anomaly_text = f"""
    Total Anomalies Detected: {len(anomalies):,} records
    Percentage of Data: {anomaly_pct:.2f}%
    Normal Records: {len(df) - len(anomalies):,}
    Quality Status: {'Good' if anomaly_pct < 5 else 'Needs Attention' if anomaly_pct < 10 else 'Critical'}
    """
    story.append(Paragraph(anomaly_text, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Trends Analysis
    if trends:
        story.append(Paragraph("TREND ANALYSIS", heading_style))
        
        trend_chart = generate_trend_chart(trends)
        if trend_chart:
            try:
                img_trend = Image(trend_chart, width=5.5*inch, height=2.75*inch)
                story.append(img_trend)
                story.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Trends table
        trend_table_data = [['Metric', 'Total Growth %', 'Monthly Growth %', 'Data Points']]
        for metric, trend_data in list(trends.items())[:5]:
            trend_table_data.append([
                metric[:20],
                f"{trend_data['total_growth_percent']:.1f}%",
                f"{trend_data['avg_monthly_growth_percent']:.1f}%",
                f"{trend_data['data_points']}"
            ])
        
        trend_table = Table(trend_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        trend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        
        story.append(trend_table)
    
    story.append(PageBreak())
    
    # Recommendations
    story.append(Paragraph("PRIORITY RECOMMENDATIONS", heading_style))
    
    if recommendations:
        for i, rec in enumerate(recommendations[:10], 1):
            priority_color = '#e74c3c' if rec['priority'] == 'High' else '#f39c12' if rec['priority'] == 'Medium' else '#27ae60'
            
            rec_title = f"{i}. [{rec['priority']}] {rec['action']}"
            story.append(Paragraph(rec_title, ParagraphStyle(
                'RecTitle',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor(priority_color),
                fontName='Helvetica-Bold',
                spaceAfter=3
            )))
            
            story.append(Paragraph(f"<b>Evidence:</b> {rec['evidence']}", body_style))
            story.append(Paragraph(f"<b>Impact:</b> {rec['impact']}", body_style))
            story.append(Spacer(1, 0.15*inch))
    
    story.append(PageBreak())
    
    # Detailed Data Tables
    story.append(Paragraph("DETAILED DATA TABLES", heading_style))
    
    # Column information
    story.append(Paragraph("Column Information", styles['Heading3']))
    
    col_data = [['Column', 'Type', 'Non-Null', 'Null']]
    for col in df.columns[:10]:
        col_data.append([
            col[:15],
            str(df[col].dtype)[:15],
            f"{df[col].count()}",
            f"{df[col].isnull().sum()}"
        ])
    
    col_table = Table(col_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    col_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ]))
    
    story.append(col_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph("This is an automatically generated report from AI Data Autopilot", footer_style))
    story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
    
    # Build PDF
    doc.build(story)
    pdf_bytes.seek(0)
    
    return pdf_bytes.getvalue()


def export_kpis_to_csv(kpis: Dict) -> str:
    """
    Export KPIs to CSV format.
    """
    if not kpis:
        return "No KPIs to export"
    
    df = pd.DataFrame(kpis).T
    return df.to_csv(index=True)


def export_anomalies_to_csv(anomalies) -> str:
    """
    Export anomalies to CSV format.
    """
    if isinstance(anomalies, pd.DataFrame):
        if len(anomalies) == 0:
            return "No anomalies to export"
        return anomalies.to_csv(index=False)
    
    return "No anomalies to export"


def export_recommendations_to_csv(recommendations: List[Dict]) -> str:
    """
    Export recommendations to CSV format.
    """
    if not recommendations:
        return "No recommendations to export"
    
    df = pd.DataFrame(recommendations)
    return df.to_csv(index=False)