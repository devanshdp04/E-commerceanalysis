import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def load_local_dataset(file_path):
    """
    Load the UK Retail Dataset from local machine
    """
    print("Loading dataset...")
    
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        print("Dataset loaded successfully!")
        return df
    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        return None
def perform_initial_cleaning(df):
    """
    Perform initial cleaning of the dataset
    """
    if df is None:
        return None
    
    print("\nInitial data shape:", df.shape)
    
    # Create a copy of the dataframe
    df_cleaned = df.copy()
    
    # Remove rows with missing values
    initial_rows = len(df_cleaned)
    df_cleaned = df_cleaned.dropna()
    print(f"Removed {initial_rows - len(df_cleaned)} rows with missing values")
    
    # Remove rows with negative quantities or prices
    valid_rows = len(df_cleaned)
    df_cleaned = df_cleaned[
        (df_cleaned['Quantity'] > 0) & 
        (df_cleaned['Price'] > 0)
    ]
    print(f"Removed {valid_rows - len(df_cleaned)} rows with negative quantities or prices")
    
    # Remove cancelled orders (those with 'C' in InvoiceNo)
    before_cancel = len(df_cleaned)
    df_cleaned = df_cleaned[~df_cleaned['Invoice'].astype(str).str.contains('C')]
    print(f"Removed {before_cancel - len(df_cleaned)} cancelled orders")
    
    # Add derived columns
    df_cleaned['TotalAmount'] = df_cleaned['Quantity'] * df_cleaned['Price']
    
    print("\nFinal data shape:", df_cleaned.shape)
    return df_cleaned
def save_processed_dataset(df, filename='uk_retail_processed.csv'):
    """
    Save the processed dataset to a CSV file
    """
    if df is not None:
        df.to_csv(filename, index=False)
        print(f"\nProcessed dataset saved as {filename}")

def explore_dataset(df):
    """
    Perform initial exploration of the dataset
    """
    if df is None:
        return
    
    print("\n=== Dataset Overview ===")
    print("-----------------------")
    
    print("\nFirst few rows:\n")
    print(df.head())
    
    print("\nData Types and Non-Null Count\n:")
    print(df.info())
    
    print("\nBasic Statistics:\n")
    print(df.describe())
    
    print("\nMissing Values:\n")
    missing_values = df.isnull().sum()
    print(missing_values[missing_values > 0])
    
    print("\nUnique Values per Column:\n")
    for column in df.columns:
        print(f"{column}: {df[column].nunique()} unique values")
    
    print("\nSample Values from Each Column:")
    for column in df.columns:
        print(f"\n{column}:")
        print(df[column].sample(5).values)

def generate_basic_insights(df):
    """
    Generate some basic insights from the data
    """
    print("\n=== Basic Insights ===")
    print("--------------------")
    
    # Time range of data
    print(f"\nDate Range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
    
    # Top 5 countries by number of transactions
    print("\nTop 5 Countries by Transactions:")
    print(df['Country'].value_counts().head())
    
    # Top 5 products by quantity sold
    print("\nTop 5 Products by Quantity Sold:")
    top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head()
    print(top_products)
    
    # Basic revenue statistics
    print("\nRevenue Statistics:")
    print(f"Total Revenue: £{df['TotalAmount'].sum():,.2f}")
    print(f"Average Transaction Value: £{df['TotalAmount'].mean():,.2f}")
    print(f"Median Transaction Value: £{df['TotalAmount'].median():,.2f}")
    
    # Number of unique customers
    print(f"\nTotal Unique Customers: {df['Customer ID'].nunique():,}")
    
    # Number of unique products
    print(f"Total Unique Products: {df['StockCode'].nunique():,}")
def main():
    # Specify your local file path
    file_path = 'online_retail_II.xlsx'  # Update this to your file path
    
    # Load the dataset
    df = load_local_dataset(file_path)
    
    if df is not None:
        # Clean the dataset
        df_cleaned = perform_initial_cleaning(df)
        
        # Save the cleaned dataset
        save_processed_dataset(df_cleaned)
        
        # Explore the dataset
        explore_dataset(df_cleaned)
        
        # Generate basic insights
        generate_basic_insights(df_cleaned)
        
        return df_cleaned
    
    return None
if __name__ == "__main__":
    df = main()