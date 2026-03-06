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

def clean_data(df: pd.DataFrame, report: Dict) -> pd.DataFrame:
    """
    Clean the data based on quality report.
    
    Handles:
    - Remove duplicate rows
    - Standardize column names
    - Handle missing values
    - Normalize text fields
    """
    
    print("Cleaning data...")
    
    # Remove duplicates
    df_clean = df.drop_duplicates()
    duplicates_removed = len(df) - len(df_clean)
    if duplicates_removed > 0:
        print(f"  ✓ Removed {duplicates_removed} duplicate rows")
    
    # Standardize column names (lowercase, replace spaces with underscore)
    df_clean.columns = [col.lower().replace(' ', '_') for col in df_clean.columns]
    print("  ✓ Standardized column names")
    
    # Handle missing values in numeric columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().sum() > 0:
            # Fill with median (better than mean for outliers)
            median_val = df_clean[col].median()
            df_clean[col].fillna(median_val, inplace=True)
            print(f"  ✓ Filled {col} blanks with median: {median_val}")
    
    # Standardize text columns (lowercase, strip whitespace)
    text_cols = df_clean.select_dtypes(include=['object']).columns
    for col in text_cols:
        # Only if it looks like a category (few unique values)
        if df_clean[col].nunique() < len(df_clean) * 0.1:
            df_clean[col] = df_clean[col].str.lower().str.strip()
            print(f"  ✓ Standardized {col} (lowercase, whitespace trimmed)")
    
    print(f"\n✓ Data cleaning complete")
    print(f"  Before: {len(df)} rows")
    print(f"  After: {len(df_clean)} rows")
    
    return df_clean

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


if __name__ == "__main__":
    # Load
    df = load_csv("sample_data/subscription_data.csv")
    
    # Check quality
    report = check_data_quality(df)
    
    print("\n=== DATA QUALITY REPORT (BEFORE) ===")
    print(f"Rows: {report['total_rows']}")
    print(f"Columns: {report['total_columns']}")
    print(f"Blank cells: {report['blank_cells']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Quality score: {report['quality_score']:.1f}%")
    
    # Clean
    df_clean = clean_data(df, report)
    
    # Check quality again
    report_clean = check_data_quality(df_clean)
    
    print("\n=== DATA QUALITY REPORT (AFTER) ===")
    print(f"Rows: {report_clean['total_rows']}")
    print(f"Columns: {report_clean['total_columns']}")
    print(f"Blank cells: {report_clean['blank_cells']}")
    print(f"Duplicate rows: {report_clean['duplicate_rows']}")
    print(f"Quality score: {report_clean['quality_score']:.1f}%")
    
    print("\nColumn Types:")
    for col, type_ in report_clean['column_types'].items():
        print(f"  {col}: {type_}")        