import pandas as pd
import numpy as np
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_etl_pipeline():
    logging.info("Starting ETL Pipeline for E-Commerce Data...")
    
    # 1. EXTRACT
    logging.info("Extracting data...")
    # In a real scenario, this loads a 500k+ row CSV
    # df = pd.read_csv('raw_data/transactions_2026.csv')
    
    # Simulating data for demonstration
    np.random.seed(42)
    n_rows = 500000
    df = pd.DataFrame({
        'transaction_id': range(1, n_rows + 1),
        'date': pd.date_range(start='2025-01-01', periods=n_rows, freq='T'),
        'product_id': np.random.randint(100, 500, size=n_rows),
        'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Toys'], size=n_rows),
        'quantity': np.random.randint(1, 10, size=n_rows),
        'unit_price': np.random.uniform(10.0, 500.0, size=n_rows),
        'region': np.random.choice(['North', 'South', 'East', 'West'], size=n_rows)
    })
    
    # 2. TRANSFORM
    logging.info("Transforming data...")
    
    # Handle missing values (simulated)
    df.dropna(inplace=True)
    
    # Calculate revenue
    df['revenue'] = df['quantity'] * df['unit_price']
    
    # Add time dimensions for PowerBI
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Aggregate data by day and region to optimize PowerBI performance
    daily_sales = df.groupby([df['date'].dt.date, 'region', 'category']).agg(
        total_transactions=('transaction_id', 'count'),
        total_quantity=('quantity', 'sum'),
        total_revenue=('revenue', 'sum')
    ).reset_index()
    
    daily_sales.rename(columns={'date': 'sales_date'}, inplace=True)
    logging.info(f"Aggregated 500k rows into {len(daily_sales)} daily summary records.")
    
    # 3. LOAD
    logging.info("Loading data into SQL Warehouse...")
    # engine = create_engine('postgresql://user:password@localhost:5432/ecommerce_db')
    # daily_sales.to_sql('fact_daily_sales', engine, if_exists='replace', index=False)
    
    logging.info("ETL Pipeline completed successfully! Data is ready for PowerBI.")

if __name__ == "__main__":
    run_etl_pipeline()
