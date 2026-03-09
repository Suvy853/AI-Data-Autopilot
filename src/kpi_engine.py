import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from typing import Dict, List

def detect_metric_columns(df: pd.DataFrame) -> Dict[str, str]:
    """
    GENERIC: Detects ANY numeric column as a metric.
    Works with ANY data type (sales, HR, healthcare, e-commerce, etc.)
    """
    metrics = {}
    
    for col in df.columns:
        if 'date' in col.lower() or 'time' in col.lower() or 'timestamp' in col.lower():
            continue
        
        if 'id' in col.lower() or '_key' in col.lower() or 'account' in col.lower():
            continue
        
        if 'type' in col.lower() or 'status' in col.lower() or 'category' in col.lower():
            continue
        
        if pd.api.types.is_numeric_dtype(df[col]):
            metrics[col] = 'numeric'
    
    return metrics

def calculate_basic_kpis(df: pd.DataFrame, metrics: Dict[str, str]) -> Dict:
    """
    GENERIC: Calculate KPIs for ANY numeric columns.
    Works with ANY data type.
    """
    kpis = {}
    
    for col, metric_type in metrics.items():
        col_data = df[col].dropna()
        
        if len(col_data) == 0:
            continue
        
        kpi_set = {
            'sum': col_data.sum(),
            'average': col_data.mean(),
            'median': col_data.median(),
            'min': col_data.min(),
            'max': col_data.max(),
            'count': len(col_data),
            'std_dev': col_data.std(),
            'missing': df[col].isnull().sum()
        }
        
        kpis[col] = kpi_set
    
    return kpis

def analyze_by_segment(df: pd.DataFrame, metrics: Dict[str, str]) -> Dict:
    """
    GENERIC: Break down ANY numeric metric by ANY categorical column.
    Works with ANY data type.
    """
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    categorical_cols = [col for col in categorical_cols 
                       if 'id' not in col.lower() and '_key' not in col.lower()]
    
    if not categorical_cols or not metrics:
        return {}
    
    breakdowns = {}
    
    for cat_col in categorical_cols:
        if df[cat_col].nunique() > 50:
            continue
        
        cat_breakdowns = {}
        
        for metric_col in metrics.keys():
            try:
                breakdown = df.groupby(cat_col)[metric_col].agg(['sum', 'count', 'mean', 'min', 'max'])
                breakdown = breakdown.sort_values('sum', ascending=False)
                cat_breakdowns[metric_col] = breakdown.to_dict()
            except:
                continue
        
        if cat_breakdowns:
            breakdowns[cat_col] = cat_breakdowns
    
    return breakdowns

def calculate_trends(df: pd.DataFrame, metrics: Dict[str, str]) -> Dict:
    """
    GENERIC: Calculate trends over time for ANY data.
    Automatically finds date column and calculates growth.
    """
    date_col = None
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_col = col
            break
        elif 'date' in col.lower() or 'time' in col.lower() or 'timestamp' in col.lower():
            try:
                pd.to_datetime(df[col])
                date_col = col
                break
            except:
                continue
    
    if date_col is None:
        return {}
    
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except:
        return {}
    
    trends = {}
    
    for metric_col in metrics.keys():
        try:
            monthly = df.groupby(df[date_col].dt.to_period('M'))[metric_col].sum()
            
            if len(monthly) < 2:
                continue
            
            first_value = monthly.iloc[0]
            last_value = monthly.iloc[-1]
            
            if first_value == 0:
                growth_rate = 0
            else:
                growth_rate = ((last_value - first_value) / first_value) * 100
            
            monthly_growth = monthly.pct_change().mean() * 100
            
            trends[metric_col] = {
                'total_growth_percent': round(growth_rate, 2),
                'avg_monthly_growth_percent': round(monthly_growth, 2),
                'first_value': first_value,
                'last_value': last_value,
                'data_points': len(monthly)
            }
        except:
            continue
    
    return trends

def detect_statistical_outliers(df: pd.DataFrame, column: str, threshold: float = 3.0):
    """
    GENERIC: Find statistical outliers using Z-score.
    Works with ANY numeric column.
    """
    try:
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        outlier_indices = np.where(z_scores > threshold)[0]
        
        if len(outlier_indices) == 0:
            return pd.DataFrame()
        
        outliers = df.iloc[outlier_indices][[column]].copy()
        outliers['z_score'] = z_scores[outlier_indices]
        return outliers.sort_values('z_score', ascending=False)
    except:
        return pd.DataFrame()

def detect_isolation_forest_outliers(df: pd.DataFrame, numeric_cols: List[str], contamination: float = 0.05):
    """
    GENERIC: Find multivariate outliers using ML.
    Works with ANY numeric columns.
    """
    try:
        if not numeric_cols:
            return pd.DataFrame()
        
        X = df[numeric_cols].fillna(df[numeric_cols].mean())
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        outlier_predictions = iso_forest.fit_predict(X)
        outliers = df[outlier_predictions == -1].copy()
        return outliers
    except:
        return pd.DataFrame()

def generate_narrative(kpis: Dict, trends: Dict, anomalies: Dict) -> str:
    """
    GENERIC: Generate narrative for ANY data type.
    No industry-specific assumptions.
    """
    narrative = []
    
    narrative.append("# Data Analysis Summary\n")
    
    if kpis:
        narrative.append("## Key Metrics\n")
        for metric_name, metric_values in list(kpis.items())[:5]:
            if 'sum' in metric_values and 'average' in metric_values:
                sum_val = metric_values['sum']
                avg_val = metric_values['average']
                narrative.append(f"**{metric_name}**: Total={sum_val:,.0f}, Average={avg_val:,.2f}\n")
            elif 'average' in metric_values:
                avg_val = metric_values['average']
                narrative.append(f"**{metric_name}**: Average={avg_val:,.2f}\n")
    
    if trends:
        narrative.append("\n## Trends\n")
        for metric, trend_data in trends.items():
            growth = trend_data['total_growth_percent']
            if growth > 5:
                narrative.append(f"✓ {metric} is growing: +{growth:.1f}%\n")
            elif growth < -5:
                narrative.append(f"⚠ {metric} is declining: {growth:.1f}%\n")
            else:
                narrative.append(f"→ {metric} is stable\n")
    
    if anomalies and len(anomalies) > 0:
        narrative.append(f"\n## Issues Found\n")
        narrative.append(f"Detected {len(anomalies)} anomalies that need investigation.\n")
    else:
        narrative.append(f"\n## Quality\n")
        narrative.append("✓ No major anomalies detected in the data.\n")
    
    return "".join(narrative)

def generate_recommendations(kpis: Dict, trends: Dict, anomalies: Dict) -> List[Dict]:
    """
    GENERIC: Generate recommendations for ANY data type.
    No industry-specific assumptions.
    """
    recommendations = []
    
    if trends:
        for metric, trend_data in trends.items():
            if trend_data['total_growth_percent'] < -10:
                recommendations.append({
                    'priority': 'HIGH',
                    'action': f'Investigate declining {metric}',
                    'evidence': f'Down {abs(trend_data["total_growth_percent"]):.1f}%',
                    'impact': f'{metric} is at risk'
                })
            elif trend_data['total_growth_percent'] > 20:
                recommendations.append({
                    'priority': 'LOW',
                    'action': f'Analyze what\'s driving {metric} growth',
                    'evidence': f'Up {trend_data["total_growth_percent"]:.1f}%',
                    'impact': 'Opportunity identified'
                })
    
    if len(anomalies) > 10:
        recommendations.append({
            'priority': 'MEDIUM',
            'action': 'Review anomalous records',
            'evidence': f'{len(anomalies)} unusual values detected',
            'impact': 'Data quality assurance'
        })
    
    if not trends:
        recommendations.append({
            'priority': 'LOW',
            'action': 'No date column found',
            'evidence': 'Cannot calculate trends without timeline',
            'impact': 'Consider adding date information'
        })
    
    return recommendations[:5]