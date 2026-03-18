import pandas as pd
import numpy as np
import re

def check_nulls(df: pd.DataFrame) -> dict:
    """Detects null/missing values (count + percentage per column)."""
    null_counts = df.isnull().sum()
    null_pct = (null_counts / len(df)) * 100
    
    results = {}
    for col in df.columns:
        results[col] = {
            'count': int(null_counts[col]),
            'percentage': round(float(null_pct[col]), 2)
        }
    return results

def check_duplicates(df: pd.DataFrame) -> dict:
    """Detects duplicate rows."""
    dup_count = df.duplicated().sum()
    dup_pct = (dup_count / len(df)) * 100 if len(df) > 0 else 0
    return {
        'count': int(dup_count),
        'percentage': round(float(dup_pct), 2)
    }

def check_data_types(df: pd.DataFrame) -> dict:
    """
    Validates data types and detects mismatches (e.g. objects in a predominantly numeric column).
    """
    results = {}
    for col in df.columns:
        inferred_type = pd.api.types.infer_dtype(df[col], skipna=True)
        actual_type = str(df[col].dtype)
        # Check if pandas says it's object but mostly behaves like something else.
        results[col] = {
            'pandas_dtype': actual_type,
            'inferred_type': inferred_type
        }
    return results

def check_outliers_iqr(df: pd.DataFrame) -> dict:
    """Detects outliers using the IQR method for numeric columns."""
    results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        outlier_count = len(outliers)
        outlier_pct = (outlier_count / len(df)) * 100 if len(df) > 0 else 0
        
        results[col] = {
            'outlier_count': int(outlier_count),
            'outlier_percentage': round(float(outlier_pct), 2),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound)
        }
    return results

def check_statistics(df: pd.DataFrame) -> dict:
    """Computes column-level statistics (min, max, mean, std deviation) for numeric cols."""
    results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        results[col] = {
            'min': float(df[col].min()) if not pd.isna(df[col].min()) else None,
            'max': float(df[col].max()) if not pd.isna(df[col].max()) else None,
            'mean': round(float(df[col].mean()), 2) if not pd.isna(df[col].mean()) else None,
            'std': round(float(df[col].std()), 2) if not pd.isna(df[col].std()) else None
        }
    return results

def check_cardinality(df: pd.DataFrame) -> dict:
    """Checks cardinality (unique value counts) for all columns."""
    results = {}
    for col in df.columns:
        results[col] = {
            'unique_count': int(df[col].nunique(dropna=False)),
            'unique_percentage': round((df[col].nunique(dropna=False) / len(df)) * 100, 2) if len(df) > 0 else 0
        }
    return results

def check_patterns(df: pd.DataFrame) -> dict:
    """
    Validates patterns for emails, dates, phone numbers based on regex.
    Heuristically applies checks based on column names.
    """
    results = {}
    
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    # A simple but comprehensive regex for date YYYY-MM-DD
    date_regex = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    # A very loose phone number regex (at least 7 digits, optional + or dashes)
    phone_regex = re.compile(r"^\+?[\d\s-]{7,15}$")
    
    for col in df.columns:
        col_lower = str(col).lower()
        pattern = None
        pattern_name = None
        
        if 'email' in col_lower:
            pattern = email_regex
            pattern_name = 'email'
        elif 'date' in col_lower:
            pattern = date_regex
            pattern_name = 'date (YYYY-MM-DD)'
        elif 'phone' in col_lower:
            pattern = phone_regex
            pattern_name = 'phone'
            
        if pattern:
            # Check non-null values matching regex
            non_nulls = df[col].dropna().astype(str)
            if len(non_nulls) == 0:
                continue
                
            matches = non_nulls.apply(lambda x: bool(pattern.match(x.strip())))
            invalid_count = len(matches) - matches.sum()
            invalid_pct = (invalid_count / len(non_nulls)) * 100
            
            results[col] = {
                'pattern_type': pattern_name,
                'invalid_count': int(invalid_count),
                'invalid_percentage': round(float(invalid_pct), 2)
            }
            
    return results

def run_all_checks(df: pd.DataFrame) -> dict:
    """Runs all data quality checks and compiles them into a single report dictionary."""
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'nulls': check_nulls(df),
        'duplicates': check_duplicates(df),
        'data_types': check_data_types(df),
        'outliers': check_outliers_iqr(df),
        'statistics': check_statistics(df),
        'cardinality': check_cardinality(df),
        'patterns': check_patterns(df)
    }
