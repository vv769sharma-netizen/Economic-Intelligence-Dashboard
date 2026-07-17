"""
Module for preprocessing raw GDP data.
"""

import sys
import logging
import pandas as pd
import numpy as np
from config import BASE_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GDPPreprocessor:
    """Class to clean and preprocess raw GDP data."""
    
    def __init__(self):
        """Initialize paths for input and output."""
        self.input_path = BASE_DIR / "data" / "raw" / "gdp_data.csv"
        self.output_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
        
    def preprocess(self) -> pd.DataFrame:
        """
        Run the preprocessing pipeline.
        
        Returns:
            pd.DataFrame: The cleaned and engineered DataFrame.
        """
        logging.info(f"Reading raw data from {self.input_path}")
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logging.error(f"Input file {self.input_path} not found.")
            sys.exit(1)
            
        # 1. Deduplicate on Country and Year
        initial_len = len(df)
        df = df.drop_duplicates(subset=["Country", "Year"], keep="first")
        logging.info(f"Dropped {initial_len - len(df)} duplicate rows.")
        
        # 2. Type conversions
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
        df["GDP_USD"] = pd.to_numeric(df["GDP_USD"], errors="coerce")
        df = df.dropna(subset=["Year", "GDP_USD"]) # Drop if year or GDP is invalid
        df["Year"] = df["Year"].astype(int)
        
        # 3. Sort by Country and Year (required before feature engineering)
        df = df.sort_values(by=["Country", "Year"]).reset_index(drop=True)
        
        # 4. Engineer Features
        df["Previous_GDP"] = df.groupby("Country")["GDP_USD"].shift(1)
        df["GDP_Difference"] = df["GDP_USD"] - df["Previous_GDP"]
        
        # Guard against divide-by-zero for growth rate
        df["GDP_Growth_Rate"] = np.where(
            (df["Previous_GDP"] == 0) | df["Previous_GDP"].isna(),
            np.nan,
            df["GDP_Difference"] / df["Previous_GDP"]
        )
        
        # 5. Fill NaNs with 0 for the first year of each country
        cols_to_fill = ["Previous_GDP", "GDP_Difference", "GDP_Growth_Rate"]
        df[cols_to_fill] = df[cols_to_fill].fillna(0)
        
        return df
        
    def run(self):
        """Execute the preprocessing and save the result."""
        df = self.preprocess()
        if not df.empty:
            df.to_csv(self.output_path, index=False)
            logging.info(f"Successfully saved {len(df)} cleaned records to {self.output_path}")
        else:
            logging.error("Pipeline failed: Preprocessed DataFrame is empty.")
            sys.exit(1)

if __name__ == "__main__":
    preprocessor = GDPPreprocessor()
    preprocessor.run()
