"""
Module for extracting GDP data from the World Bank API.
"""

import sys
import logging
import requests
import pandas as pd
from config import WORLD_BANK_API_URL, BASE_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GDPDataExtractor:
    """Class to extract and process raw GDP data from the World Bank API."""
    
    def __init__(self):
        """Initialize the extractor with the API URL and output path."""
        self.api_url = WORLD_BANK_API_URL
        self.output_path = BASE_DIR / "data" / "raw" / "gdp_data.csv"
        
    def fetch_data(self) -> list:
        """
        Fetch data from the API.
        
        Returns:
            list: The records portion of the JSON response, or empty list on failure.
        """
        logging.info(f"Fetching data from {self.api_url}")
        try:
            response = requests.get(self.api_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            # World Bank API returns [pagination_metadata, records]
            if len(data) >= 2 and data[1] is not None:
                return data[1]
            else:
                logging.warning("API returned unexpected format or empty records.")
                return []
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error or bad response during fetch: {e}")
            return []
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return []
            
    def process_data(self, records: list) -> pd.DataFrame:
        """
        Convert raw records to a DataFrame, keeping only necessary columns and dropping NaNs.
        
        Args:
            records (list): The raw JSON records.
            
        Returns:
            pd.DataFrame: The processed DataFrame.
        """
        if not records:
            logging.warning("No records to process.")
            return pd.DataFrame()
            
        df = pd.DataFrame(records)
        
        # Extract country name and code safely (since it's a nested dict)
        if "country" in df.columns:
            df["Country"] = df["country"].apply(lambda x: x.get("value") if isinstance(x, dict) else None)
            df["Country_Code"] = df["countryiso3code"]
        else:
            logging.error("Expected 'country' column not found in data.")
            return pd.DataFrame()
            
        df["Year"] = df["date"]
        df["GDP_USD"] = df["value"]
        
        # Keep only desired columns
        keep_cols = ["Country", "Country_Code", "Year", "GDP_USD"]
        df = df[[col for col in keep_cols if col in df.columns]]
        
        # Drop rows where GDP_USD is null
        df = df.dropna(subset=["GDP_USD"])
        
        return df
        
    def run(self):
        """Execute the extraction pipeline and save to CSV."""
        records = self.fetch_data()
        df = self.process_data(records)
        
        if not df.empty:
            df.to_csv(self.output_path, index=False)
            logging.info(f"Successfully saved {len(df)} records to {self.output_path}")
        else:
            logging.error("Pipeline failed: DataFrame is empty. No data saved.")
            sys.exit(1)

if __name__ == "__main__":
    extractor = GDPDataExtractor()
    extractor.run()
