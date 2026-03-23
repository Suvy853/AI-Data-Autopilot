import pandas as pd
import numpy as np
from typing import Dict, List

def detect_important_segments(df: pd.DataFrame, metrics: Dict) -> Dict:
    """
    Auto-detect important segments (categorical columns with reasonable cardinality).
    Works with any B2B dataset.
    """
    segments = {}
    
    # Find categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in categorical_cols:
        # Skip ID columns
        if 'id' in col.lower() or '_key' in col.lower() or 'account' in col.lower():
            continue
        
        # Only include columns with 2-20 unique values (true segments)
        unique_count = df[col].nunique()
        if 2 <= unique_count <= 20:
            segment_data = {}
            total_records = len(df)
            
            for segment_value in df[col].unique():
                segment_count = len(df[df[col] == segment_value])
                segment_percentage = (segment_count / total_records) * 100
                
                segment_data[segment_value] = {
                    'count': segment_count,
                    'percentage': segment_percentage
                }
            
            segments[col] = segment_data
    
    return segments


def generate_business_insights(df: pd.DataFrame, kpis: Dict, trends: Dict, 
                               anomalies: pd.DataFrame, segments: Dict) -> str:
    """
    Generate PURE PROSE business insights - NO special characters, NO markdown, NO bullets.
    Each insight is a flowing paragraph of professional business analysis.
    """
    insights = []
    
    # ============================================
    # DATA QUALITY ASSESSMENT
    # ============================================
    total_records = len(df)
    quality_percentage = 100 - (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    
    insights.append("Data Quality Assessment")
    insights.append("")
    
    if quality_percentage >= 95:
        insights.append("The dataset exhibits excellent quality with a score of {:.1f} percent. Data is clean, reliable, and ready for comprehensive analysis. No significant quality issues were detected during assessment.".format(quality_percentage))
    elif quality_percentage >= 80:
        insights.append("The dataset demonstrates good quality with a score of {:.1f} percent. Data has been appropriately cleaned and is suitable for analytical work. Minor quality issues were identified and addressed.".format(quality_percentage))
    else:
        insights.append("The dataset requires attention with a quality score of {:.1f} percent. Significant data inconsistencies were found and addressed during the cleaning process. Proceed with enhanced validation.".format(quality_percentage))
    
    # ============================================
    # KEY PERFORMANCE INDICATORS
    # ============================================
    if kpis:
        insights.append("")
        insights.append("")
        insights.append("Key Performance Indicators")
        insights.append("")
        
        # Find top metrics by sum
        top_metrics = sorted(kpis.items(), key=lambda x: x[1].get('sum', 0), reverse=True)[:3]
        metric_names = []
        for name, _ in top_metrics:
            metric_names.append(name.replace('_', ' ').title())
        
        metrics_text = "The analysis identified {} key performance indicators in the dataset. Primary metrics include {}. These metrics represent the core quantitative measures of business performance.".format(
            len(kpis),
            ", ".join(metric_names)
        )
        insights.append(metrics_text)
    
    # ============================================
    # SEGMENT ANALYSIS
    # ============================================
    if segments:
        insights.append("")
        insights.append("")
        insights.append("Segment Analysis")
        insights.append("")
        
        segment_descriptions = []
        
        for segment_col, segment_data in segments.items():
            # Calculate variation
            counts = [s['count'] for s in segment_data.values()]
            
            largest_segment = max(segment_data.items(), key=lambda x: x[1]['count'])
            smallest_segment = min(segment_data.items(), key=lambda x: x[1]['count'])
            
            size_ratio = largest_segment[1]['count'] / smallest_segment[1]['count']
            
            col_name = segment_col.replace('_', ' ').title()
            largest_name = largest_segment[0]
            smallest_name = smallest_segment[0]
            largest_pct = largest_segment[1]['percentage']
            smallest_pct = smallest_segment[1]['percentage']
            
            if size_ratio > 3:
                balance_text = "shows high imbalance with a {} times variation between largest and smallest segments".format(round(size_ratio, 1))
            else:
                balance_text = "demonstrates balanced distribution across segments"
            
            segment_desc = "The {} segment {} with {} representing {:.1f} percent (largest) and {} at {:.1f} percent (smallest).".format(
                col_name,
                balance_text,
                largest_name,
                largest_pct,
                smallest_name,
                smallest_pct
            )
            segment_descriptions.append(segment_desc)
        
        segments_text = " ".join(segment_descriptions)
        insights.append(segments_text)
    
    # ============================================
    # TREND ANALYSIS
    # ============================================
    if trends:
        insights.append("")
        insights.append("")
        insights.append("Growth and Trend Analysis")
        insights.append("")
        
        growth_metrics = []
        decline_metrics = []
        stable_metrics = []
        
        for metric, trend_data in trends.items():
            growth_pct = trend_data['total_growth_percent']
            metric_display = metric.replace('_', ' ').title()
            
            if growth_pct > 10:
                growth_metrics.append((metric_display, growth_pct))
            elif growth_pct < -10:
                decline_metrics.append((metric_display, growth_pct))
            else:
                stable_metrics.append((metric_display, growth_pct))
        
        trend_descriptions = []
        
        if growth_metrics:
            growth_text = "Growing metrics include {} showing positive momentum.".format(
                ", ".join(["{} at {:.1f} percent growth".format(m, g) for m, g in sorted(growth_metrics, key=lambda x: x[1], reverse=True)])
            )
            trend_descriptions.append(growth_text)
        
        if decline_metrics:
            decline_text = "Declining metrics include {} requiring attention and investigation.".format(
                ", ".join(["{} at {:.1f} percent decline".format(m, abs(d)) for m, d in sorted(decline_metrics, key=lambda x: x[1])])
            )
            trend_descriptions.append(decline_text)
        
        if stable_metrics:
            stable_metric_names = ", ".join([m for m, _ in stable_metrics[:3]])
            stable_text = "Stable metrics including {} demonstrate consistent performance.".format(stable_metric_names)
            trend_descriptions.append(stable_text)
        
        trends_text = " ".join(trend_descriptions)
        insights.append(trends_text)
    
    # ============================================
    # ANOMALY ASSESSMENT
    # ============================================
    if anomalies is not None and not anomalies.empty:
        anomaly_pct = (len(anomalies) / len(df)) * 100
        
        insights.append("")
        insights.append("")
        insights.append("Data Anomalies and Outliers")
        insights.append("")
        
        if anomaly_pct < 1:
            anomaly_text = "Anomaly detection identified {} anomalous records representing {:.2f} percent of the dataset. The low anomaly rate indicates high data reliability and consistency across the dataset.".format(len(anomalies), anomaly_pct)
        elif anomaly_pct < 5:
            anomaly_text = "Anomaly detection identified {} anomalous records representing {:.2f} percent of the dataset. The moderate anomaly rate is acceptable for most business applications. These records deviate from expected patterns and may warrant further investigation to understand underlying causes.".format(len(anomalies), anomaly_pct)
        else:
            anomaly_text = "Anomaly detection identified {} anomalous records representing {:.2f} percent of the dataset. The elevated anomaly rate suggests data quality issues that should be addressed before proceeding with advanced analytical work.".format(len(anomalies), anomaly_pct)
        
        insights.append(anomaly_text)
    else:
        insights.append("")
        insights.append("")
        insights.append("Data Quality Assessment")
        insights.append("")
        insights.append("No significant anomalies were detected. The dataset appears consistent with expected patterns, indicating reliable data quality suitable for analytical applications.")
    
    # ============================================
    # EXECUTIVE READINESS
    # ============================================
    insights.append("")
    insights.append("")
    insights.append("Executive Readiness Summary")
    insights.append("")
    
    readiness_score = 0
    if quality_percentage >= 90:
        readiness_score += 30
    elif quality_percentage >= 80:
        readiness_score += 20
    else:
        readiness_score += 10
    
    if trends and any(abs(t['total_growth_percent']) > 0 for t in trends.values()):
        readiness_score += 25
    else:
        readiness_score += 10
    
    if anomalies is None or len(anomalies) < len(df) * 0.05:
        readiness_score += 25
    else:
        readiness_score += 10
    
    if segments:
        readiness_score += 20
    else:
        readiness_score += 10
    
    if readiness_score >= 80:
        insights.append("Status: Ready for Analysis. The dataset demonstrates sufficient quality and structure to support advanced analytical work. Data quality and organizational characteristics are conducive to comprehensive business analytics.")
    elif readiness_score >= 60:
        insights.append("Status: Conditionally Ready. The dataset is usable for analysis with consideration of identified data characteristics. Enhanced validation and monitoring during analytical work is recommended.")
    else:
        insights.append("Status: Needs Preparation. The dataset requires additional work before undertaking advanced analytical projects. Address identified data quality issues before proceeding.")
    
    return "\n".join(insights)


def generate_business_recommendations(kpis: Dict, trends: Dict, anomalies: pd.DataFrame, 
                                      df: pd.DataFrame, segments: Dict) -> List[Dict]:
    """
    Generate recommendations based on actual data patterns.
    Pure prose descriptions, NO special characters, NO markdown.
    """
    recommendations = []
    
    # ============================================
    # ANOMALY-BASED RECOMMENDATIONS
    # ============================================
    if anomalies is not None and not anomalies.empty:
        anomaly_pct = (len(anomalies) / len(df)) * 100
        
        if anomaly_pct > 5:
            recommendations.append({
                'priority': 'High',
                'action': 'Investigate data collection and entry processes for potential improvements',
                'evidence': '{} anomalous records detected, representing {:.1f} percent of the dataset'.format(len(anomalies), anomaly_pct),
                'impact': 'Prevents corrupted or unreliable data from influencing business decisions',
                'metric': 'Data Quality',
                'segment': 'General'
            })
        elif anomaly_pct > 1:
            recommendations.append({
                'priority': 'Medium',
                'action': 'Review anomalous records to identify patterns and root causes',
                'evidence': '{} outliers identified in the dataset'.format(len(anomalies)),
                'impact': 'Ensures analytical conclusions are based on reliable data patterns',
                'metric': 'Data Quality',
                'segment': 'General'
            })
    
    # ============================================
    # TREND-BASED RECOMMENDATIONS
    # ============================================
    if trends:
        for metric, trend_data in trends.items():
            growth_pct = trend_data['total_growth_percent']
            metric_display = metric.replace('_', ' ').title()
            
            if growth_pct < -20:
                recommendations.append({
                    'priority': 'High',
                    'action': 'Investigate root causes of {} decline and develop mitigation strategy'.format(metric_display),
                    'evidence': '{} declined {:.1f} percent over the analysis period'.format(metric_display, abs(growth_pct)),
                    'impact': 'Significant business risk if negative trend continues unchecked',
                    'metric': metric_display,
                    'segment': 'General'
                })
            elif growth_pct < -5:
                recommendations.append({
                    'priority': 'Medium',
                    'action': 'Analyze contributing factors to {} decline'.format(metric_display),
                    'evidence': '{} decreased {:.1f} percent during the period'.format(metric_display, abs(growth_pct)),
                    'impact': 'Understanding causes allows for proactive corrective action',
                    'metric': metric_display,
                    'segment': 'General'
                })
            elif growth_pct > 20:
                recommendations.append({
                    'priority': 'Low',
                    'action': 'Identify and reinforce drivers of {} growth'.format(metric_display),
                    'evidence': '{} growing at {:.1f} percent demonstrating positive momentum'.format(metric_display, growth_pct),
                    'impact': 'Scaling successful approaches maximizes competitive advantage',
                    'metric': metric_display,
                    'segment': 'General'
                })
    
    # ============================================
    # SEGMENT-BASED RECOMMENDATIONS
    # ============================================
    if segments:
        for segment_col, segment_data in segments.items():
            counts = [s['count'] for s in segment_data.values()]
            
            if counts:
                avg_count = np.mean(counts)
                high_variance = np.std(counts) / avg_count if avg_count > 0 else 0
                
                if high_variance > 0.5:
                    largest = max(segment_data.items(), key=lambda x: x[1]['count'])
                    smallest = min(segment_data.items(), key=lambda x: x[1]['count'])
                    ratio = largest[1]['count'] / smallest[1]['count']
                    
                    col_display = segment_col.replace('_', ' ').title()
                    
                    recommendations.append({
                        'priority': 'Medium',
                        'action': 'Analyze {} distribution and imbalance patterns'.format(col_display),
                        'evidence': '{} is {:.1f} times larger than {}, indicating significant distribution variance'.format(largest[0], ratio, smallest[0]),
                        'impact': 'Understanding distribution patterns informs resource allocation and strategic focus',
                        'metric': col_display,
                        'segment': col_display
                    })
    
    # ============================================
    # KPI VARIATION RECOMMENDATIONS
    # ============================================
    if kpis:
        for metric_name, kpi_data in kpis.items():
            if kpi_data.get('std_dev', 0) > 0 and kpi_data.get('average', 0) > 0:
                cv = kpi_data['std_dev'] / kpi_data['average']
                
                if cv > 1:
                    metric_display = metric_name.replace('_', ' ').title()
                    
                    recommendations.append({
                        'priority': 'Medium',
                        'action': 'Understand drivers of {} variation and implement optimization strategies'.format(metric_display),
                        'evidence': '{} demonstrates high variability with coefficient of variation of {:.2f}'.format(metric_display, cv),
                        'impact': 'Identifying and reducing variability improves operational consistency and predictability',
                        'metric': metric_display,
                        'segment': 'General'
                    })
    
    # ============================================
    # DEFAULT RECOMMENDATION
    # ============================================
    if not recommendations:
        recommendations.append({
            'priority': 'Low',
            'action': 'Proceed with detailed analytical investigation',
            'evidence': 'Dataset demonstrates acceptable quality and structure with no critical issues detected',
            'impact': 'Ready to move forward with advanced analytical work and strategic analysis',
            'metric': 'Overall',
            'segment': 'General'
        })
    
    # Sort by priority
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return recommendations[:10]