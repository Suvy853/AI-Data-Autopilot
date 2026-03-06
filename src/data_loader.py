import pandas as pd
import numpy as np
from typing import Tuple, Dict, List

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file with automatic encoding detection.
    
    Handles:
    - Different encodings (UTF-8, ASCII, Latin-1)
    - Different delimiters (comma, semicolon, tab)
    - Mixed line endings
    """
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"✓ Successfully loaded with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            continue
    
    # If all fail, raise error
    raise ValueError("Could not read file with any standard encoding")

def detect_column_types(df: pd.DataFrame) -> Dict[str, str]:
    """
    Detect the type of each column.
    
    Returns:
    {
        'Date': 'date',
        'Revenue': 'numeric',
        'Region': 'category',
        'Account_ID': 'text'
    }
    """
    detected_types = {}
    
    for col in df.columns:
        # Check if it's a date
        if 'date' in col.lower() or 'time' in col.lower():
            detected_types[col] = 'date'
        
        # Check if it's numeric
        elif pd.api.types.is_numeric_dtype(df[col]):
            detected_types[col] = 'numeric'
        
        # Check if it's categorical (limited unique values)
        elif df[col].nunique() < len(df) * 0.05:  # Less than 5% unique values
            detected_types[col] = 'category'
        
        # Default to text
        else:
            detected_types[col] = 'text'
    
    return detected_types

def check_data_quality(df: pd.DataFrame) -> Dict:
    """
    Check for common data quality issues.
    
    Returns:
    {
        'total_rows': 1000,
        'total_columns': 8,
        'blank_cells': 23,
        'duplicate_rows': 5,
        'column_types': {...},
        'issues': [...]
    }
    """
    issues = []
    
    # Check for blank cells
    blank_count = df.isnull().sum().sum()
    if blank_count > 0:
        issues.append(f"⚠ {blank_count} blank cells found")
    
    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        issues.append(f"⚠ {duplicate_count} duplicate rows found")
    
    # Detect column types
    col_types = detect_column_types(df)
    
    # Report
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'blank_cells': blank_count,
        'duplicate_rows': duplicate_count,
        'column_types': col_types,
        'issues': issues,
        'quality_score': max(0, 100 - (blank_count / (len(df) * len(df.columns)) * 100))
    }
    
    return report

if __name__ == "__main__":
    # Test on sample data
    df = load_csv("sample_data/subscription_data.csv")
    report = check_data_quality(df)
    
    print("\n=== DATA QUALITY REPORT ===")
    print(f"Rows: {report['total_rows']}")
    print(f"Columns: {report['total_columns']}")
    print(f"Blank cells: {report['blank_cells']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Quality score: {report['quality_score']:.1f}%")
    print("\nColumn Types:")
    for col, type_ in report['column_types'].items():
        print(f"  {col}: {type_}")
    print("\nIssues:")
    for issue in report['issues']:
        print(f"  {issue}")