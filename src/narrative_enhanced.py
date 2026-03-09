import pandas as pd
import numpy as np
from typing import Dict, List


def detect_important_segments(df: pd.DataFrame, metrics: Dict) -> Dict:
    """
    Auto-detect important segments (categories, groups) in the data.
    
    Returns segments with segment name, metrics, and patterns.
    """
    
    segments = {}
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if not categorical_cols:
        return segments
    
    metric_cols = list(metrics.keys()) if metrics else []
    
    for cat_col in categorical_cols[:3]:
        try:
            unique_count = df[cat_col].nunique()
            
            if 2 <= unique_count <= 20:
                segment_data = {}
                
                for segment_value in df[cat_col].unique()[:5]:
                    segment_df = df[df[cat_col] == segment_value]
                    
                    if len(segment_df) > 0:
                        segment_info = {
                            'count': len(segment_df),
                            'percentage': (len(segment_df) / len(df) * 100),
                            'metrics': {}
                        }
                        
                        for metric_col in metric_cols[:3]:
                            if metric_col in segment_df.columns:
                                segment_info['metrics'][metric_col] = {
                                    'average': segment_df[metric_col].mean(),
                                    'total': segment_df[metric_col].sum(),
                                    'min': segment_df[metric_col].min(),
                                    'max': segment_df[metric_col].max()
                                }
                        
                        segment_data[str(segment_value)] = segment_info
                
                if segment_data:
                    segments[cat_col] = segment_data
        
        except Exception as e:
            continue
    
    return segments


def find_segment_anomalies(df: pd.DataFrame, anomalies: pd.DataFrame, 
                          categorical_cols: List[str]) -> Dict:
    """
    Identify which segments have the most anomalies.
    
    Returns segments with anomaly counts and percentages.
    """
    
    segment_anomalies = {}
    
    if len(anomalies) == 0:
        return segment_anomalies
    
    for cat_col in categorical_cols[:3]:
        try:
            if cat_col in df.columns:
                total_by_segment = df[cat_col].value_counts()
                anomaly_by_segment = anomalies[cat_col].value_counts()
                
                segment_info = {}
                for segment in anomaly_by_segment.index[:5]:
                    total = total_by_segment.get(segment, 0)
                    anomaly_count = anomaly_by_segment.get(segment, 0)
                    
                    if total > 0:
                        anomaly_pct = (anomaly_count / total * 100)
                        segment_info[str(segment)] = {
                            'anomalies': int(anomaly_count),
                            'total_records': int(total),
                            'anomaly_percentage': anomaly_pct
                        }
                
                if segment_info:
                    segment_anomalies[cat_col] = segment_info
        
        except Exception as e:
            continue
    
    return segment_anomalies


def generate_business_insights(df: pd.DataFrame, kpis: Dict, trends: Dict, 
                              anomalies: pd.DataFrame, segments: Dict) -> str:
    """
    Generate business-focused insights instead of just technical facts.
    
    Focuses on:
    - Segment performance
    - Growth drivers
    - Problem areas
    - Opportunities
    """
    
    insights = "## Key Business Insights\n\n"
    
    # Overall performance insight
    insights += "### Overall Performance\n"
    if kpis:
        metric_names = list(kpis.keys())[:3]
        insights += f"Analyzed {len(df):,} records across {len(metric_names)} key metrics. "
        
        growth_metrics = sum(1 for trend in trends.values() 
                            if trend.get('total_growth_percent', 0) > 0)
        insights += f"{growth_metrics} metrics show positive growth trends. "
        insights += "\n\n"
    
    # Segment performance insights
    if segments:
        insights += "### Segment Performance\n"
        for segment_col, segment_data in list(segments.items())[:2]:
            insights += f"**By {segment_col}:**\n"
            
            best_segment = max(segment_data.items(), 
                             key=lambda x: len(x[1].get('metrics', {})))
            if best_segment:
                insights += f"- {best_segment[0]} is the primary segment ({best_segment[1]['percentage']:.1f}% of data)\n"
            
            insights += "\n"
    
    # Anomaly insights with business context
    if len(anomalies) > 0:
        anomaly_pct = (len(anomalies) / len(df) * 100)
        insights += "### Data Quality & Anomalies\n"
        
        if anomaly_pct < 2:
            insights += f"Excellent data quality: Only {anomaly_pct:.2f}% anomalous records detected. "
            insights += "Data is highly reliable for decision-making.\n\n"
        elif anomaly_pct < 5:
            insights += f"Good data quality: {anomaly_pct:.2f}% anomalous records detected. "
            insights += "Minor data quality issues that should be monitored.\n\n"
        else:
            insights += f"Attention needed: {anomaly_pct:.2f}% anomalous records detected. "
            insights += "Investigate root causes and implement data quality improvements.\n\n"
    
    # Growth opportunities
    if trends:
        insights += "### Growth Opportunities\n"
        positive_trends = [m for m, t in trends.items() 
                          if t.get('total_growth_percent', 0) > 10]
        if positive_trends:
            insights += f"Strong growth identified in: {', '.join(positive_trends[:3])}. "
            insights += "Consider increasing focus on these areas.\n\n"
    
    # Risk areas
    if len(anomalies) > 0:
        insights += "### Areas Requiring Attention\n"
        insights += f"- {len(anomalies):,} anomalous records need investigation\n"
        insights += f"- Review data cleaning and quality processes\n"
        insights += "- Implement additional validation rules\n\n"
    
    return insights


def generate_business_recommendations(kpis: Dict, trends: Dict, 
                                     anomalies: pd.DataFrame, df: pd.DataFrame,
                                     segments: Dict) -> List[Dict]:
    """
    Generate business-focused recommendations with evidence.
    
    Each recommendation includes:
    - Action (what to do)
    - Priority (High/Medium/Low)
    - Evidence (why)
    - Impact (business benefit)
    - Segment (where applicable)
    """
    
    recommendations = []
    
    # Recommendation 1: Data Quality
    anomaly_pct = (len(anomalies) / len(df) * 100) if len(df) > 0 else 0
    if anomaly_pct > 5:
        recommendations.append({
            'priority': 'High',
            'action': 'Implement data quality improvements and validation rules',
            'evidence': f'{anomaly_pct:.2f}% of records are anomalous, indicating potential data issues',
            'impact': 'Ensure data reliability, improve decision-making accuracy, reduce false insights',
            'segment': 'Data Operations',
            'metric': f'{len(anomalies):,} anomalies detected'
        })
    
    # Recommendation 2: Segment Focus
    if segments:
        best_segment_col = list(segments.keys())[0] if segments else None
        if best_segment_col and segments[best_segment_col]:
            best_segment = max(segments[best_segment_col].items(), 
                             key=lambda x: x[1].get('percentage', 0))
            recommendations.append({
                'priority': 'High',
                'action': f'Prioritize growth in {best_segment[0]} segment',
                'evidence': f'{best_segment[1]["percentage"]:.1f}% of customer base, highest concentration',
                'impact': 'Focus resources on highest value segment, maximize ROI',
                'segment': best_segment_col,
                'metric': f'{best_segment[1]["count"]:,} records'
            })
    
    # Recommendation 3: Growth Metrics
    if trends:
        growth_metrics = [(m, t['total_growth_percent']) for m, t in trends.items() 
                         if t.get('total_growth_percent', 0) > 0]
        if growth_metrics:
            top_growth = max(growth_metrics, key=lambda x: x[1])
            recommendations.append({
                'priority': 'High',
                'action': f'Accelerate investment in {top_growth[0]} (top growth driver)',
                'evidence': f'{top_growth[1]:.1f}% growth identified, strongest performer',
                'impact': 'Capitalize on momentum, increase market share, boost revenue',
                'segment': 'Strategic',
                'metric': f'{top_growth[1]:.1f}% growth rate'
            })
    
    # Recommendation 4: Underperforming Areas
    if trends:
        negative_trends = [(m, t['total_growth_percent']) for m, t in trends.items() 
                          if t.get('total_growth_percent', 0) < -5]
        if negative_trends:
            worst_trend = min(negative_trends, key=lambda x: x[1])
            recommendations.append({
                'priority': 'Medium',
                'action': f'Investigate decline in {worst_trend[0]}',
                'evidence': f'{worst_trend[1]:.1f}% negative growth trend detected',
                'impact': 'Identify root causes, prevent further decline, stabilize metrics',
                'segment': 'Analysis',
                'metric': f'{worst_trend[1]:.1f}% decline'
            })
    
    # Recommendation 5: Monitoring
    if kpis:
        recommendations.append({
            'priority': 'Medium',
            'action': 'Establish KPI monitoring dashboard for real-time tracking',
            'evidence': f'{len(kpis)} key metrics identified, multiple growth trends',
            'impact': 'Enable proactive decision-making, faster response to issues',
            'segment': 'Reporting',
            'metric': f'{len(kpis)} metrics'
        })
    
    return recommendations


def format_anomalies_for_display(anomalies: pd.DataFrame) -> pd.DataFrame:
    """
    Format anomalies table for better display and analysis.
    
    Adds:
    - Anomaly score
    - Severity level
    - Key metrics
    """
    
    if len(anomalies) == 0:
        return pd.DataFrame()
    
    display_df = anomalies.copy()
    
    # Add severity level based on z-score if available
    if 'z_score' in display_df.columns:
        display_df['Severity'] = display_df['z_score'].apply(
            lambda x: 'Critical' if abs(x) > 4 else 'High' if abs(x) > 3 else 'Medium'
        )
    
    # Reorder columns to show most important first
    cols = display_df.columns.tolist()
    priority_cols = ['Severity'] if 'Severity' in cols else []
    priority_cols += [c for c in ['z_score', 'anomaly_score'] if c in cols]
    
    other_cols = [c for c in cols if c not in priority_cols]
    display_df = display_df[priority_cols + other_cols]
    
    return display_df