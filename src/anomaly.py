import pandas as pd
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from typing import List

def detect_statistical_outliers(df: pd.DataFrame, column: str, threshold: float = 3.0):
    """Find outliers using Z-score"""
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
    """Find outliers using ML"""
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

def find_category_anomalies(df: pd.DataFrame, category_col: str, metric_col: str) -> dict:
    """Find categories that are unusual"""
    try:
        grouped = df.groupby(category_col)[metric_col].agg(['sum', 'count', 'mean'])
        
        mean_sum = grouped['sum'].mean()
        std_sum = grouped['sum'].std()
        
        anomalies = {}
        
        for category, row in grouped.iterrows():
            if row['sum'] > mean_sum + (2 * std_sum):
                anomalies[category] = {
                    'type': 'unusually_high',
                    'value': row['sum'],
                    'vs_average': row['sum'] / mean_sum,
                    'count': row['count']
                }
            elif row['sum'] < mean_sum - (2 * std_sum):
                anomalies[category] = {
                    'type': 'unusually_low',
                    'value': row['sum'],
                    'vs_average': row['sum'] / mean_sum,
                    'count': row['count']
                }
        
        return anomalies
    except:
        return {}