import pandas as pd
import os

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.
    
    Args:
        filepath (str): The absolute or relative path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded DataFrame.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a CSV.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    if not filepath.lower().endswith('.csv'):
        raise ValueError("Only CSV files are supported currently.")
        
    try:
        # We read as string initially for pattern checks, but let pandas infer first 
        # and we can handle mixed types more gracefully if we let it infer.
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV file: {str(e)}")
