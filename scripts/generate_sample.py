import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data(file_name="sample_financial_data.csv", num_rows=1000):
    """
    Generates a mock financial dataset simulating realistic errors:
    - Null values
    - Duplicates
    - Data type inconsistencies
    - Outliers
    - Invalid emails and dates
    """
    print(f"Generating {num_rows} rows of sample data...")
    
    # Initialize random seeder for reproducibility
    np.random.seed(42)
    random.seed(42)

    # 1. Base Data Generation
    transaction_ids = [f"TXN-{i:05d}" for i in range(1, num_rows + 1)]
    
    # Dates between 2023-01-01 and 2023-12-31
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=random.randint(0, 364)) for _ in range(num_rows)]
    date_strs = [d.strftime('%Y-%m-%d') for d in dates]
    
    amounts = np.round(np.random.normal(500, 150, num_rows), 2)
    amounts = np.clip(amounts, 10, None)  # Ensure no negative amounts
    
    categories = ['Grocery', 'Utility', 'Entertainment', 'Healthcare', 'Travel']
    category_col = np.random.choice(categories, num_rows)
    
    statuses = ['Completed', 'Pending', 'Failed']
    status_col = np.random.choice(statuses, num_rows, p=[0.8, 0.15, 0.05])
    
    emails = [f"user{i}@example.com" for i in range(1, num_rows + 1)]
    
    phones = [f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}" for _ in range(num_rows)]

    # 2. Inject Errors / Data Quality Issues
    
    # Inject Nulls (5% in amount, 2% in category)
    amount_null_indices = np.random.choice(num_rows, int(num_rows * 0.05), replace=False)
    amounts[amount_null_indices] = np.nan
    
    cat_null_indices = np.random.choice(num_rows, int(num_rows * 0.02), replace=False)
    category_col[cat_null_indices] = None

    # Inject Duplicates (copy some rows and append them)
    df = pd.DataFrame({
        'Transaction_ID': transaction_ids,
        'Date': date_strs,
        'Amount': amounts,
        'Category': category_col,
        'Status': status_col,
        'Customer_Email': emails,
        'Customer_Phone': phones
    })
    
    dup_rows = df.sample(int(num_rows * 0.03)) # 3% duplicates
    df = pd.concat([df, dup_rows], ignore_index=True)
    
    # Inject Data Type inconsistencies (Strings in numeric column)
    str_amount_indices = np.random.choice(len(df), int(len(df) * 0.01), replace=False)
    for idx in str_amount_indices:
        if not pd.isna(df.at[idx, 'Amount']):
            df.at[idx, 'Amount'] = "ONE HUNDRED"

    # Inject Outliers (Amounts > 5000)
    outlier_indices = np.random.choice(len(df), int(len(df) * 0.01), replace=False)
    for idx in outlier_indices:
        if df.at[idx, 'Amount'] != "ONE HUNDRED":
             df.at[idx, 'Amount'] = float(random.randint(5000, 15000))

    # Inject Invalid Patterns (emails without @, malformed dates)
    invalid_email_indices = np.random.choice(len(df), int(len(df) * 0.02), replace=False)
    for idx in invalid_email_indices:
        df.at[idx, 'Customer_Email'] = df.at[idx, 'Customer_Email'].replace("@", "")

    invalid_date_indices = np.random.choice(len(df), int(len(df) * 0.02), replace=False)
    for idx in invalid_date_indices:
        df.at[idx, 'Date'] = "2023/13/45"
        
    invalid_phone_indices = np.random.choice(len(df), int(len(df) * 0.02), replace=False)
    for idx in invalid_phone_indices:
        df.at[idx, 'Customer_Phone'] = "12345" # too short

    # Shuffle the dataframe
    df = df.sample(frac=1).reset_index(drop=True)

    # Save to CSV
    df.to_csv(file_name, index=False)
    print(f"Dataset successfully saved to {file_name} with {len(df)} rows.")

if __name__ == "__main__":
    generate_sample_data()
