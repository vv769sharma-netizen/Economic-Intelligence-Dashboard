"""
Module to load processed GDP data into the MySQL database.
"""

import sys
import logging
import pandas as pd
from sqlalchemy import text
from config import BASE_DIR
import sys
import os

# Add parent dir to sys.path so we can import from database package easily
sys.path.append(str(BASE_DIR))

from database.db_connection import DatabaseConnection

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseLoader:
    """Class to handle loading data into the database."""
    
    def __init__(self):
        """Initialize paths."""
        self.input_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
        
    def load_data(self):
        """Execute the loading process."""
        logging.info(f"Reading processed data from {self.input_path}")
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logging.error(f"Input file {self.input_path} not found. Please run preprocess.py first.")
            sys.exit(1)
            
        # Rename columns to match lowercase schema
        df = df.rename(columns={
            "Country": "country",
            "Country_Code": "country_code",
            "Year": "year",
            "GDP_USD": "gdp_usd",
            "Previous_GDP": "previous_gdp",
            "GDP_Difference": "gdp_difference",
            "GDP_Growth_Rate": "gdp_growth_rate"
        })
        
        engine = DatabaseConnection.get_engine()
        table_name = "gdp_data"
        
        try:
            with engine.begin() as conn: # Transactional block
                # Clear existing rows idempotently
                logging.info(f"Clearing existing data from table '{table_name}'.")
                conn.execute(text(f"TRUNCATE TABLE {table_name}"))
                
                # Insert data
                logging.info("Inserting new data...")
                df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
                
            logging.info(f"Successfully inserted {len(df)} rows into {table_name}.")
        except Exception as e:
            logging.error(f"Database operation failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    loader = DatabaseLoader()
    loader.load_data()
