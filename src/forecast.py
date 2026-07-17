"""
Module for forecasting GDP for a chosen country iteratively.
"""

import sys
import logging
import pickle
import pandas as pd
import numpy as np
from config import BASE_DIR, MODEL_PATH, FEATURES

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GDPForecaster:
    """Class to forecast future GDP iteratively."""
    
    def __init__(self):
        """Initialize and load the model."""
        self.input_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
        try:
            with open(MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            logging.error(f"Model file {MODEL_PATH} not found. Please train the model first.")
            self.model = None
            
    def forecast(self, country: str, years_ahead: int = 5) -> pd.DataFrame:
        """
        Forecast GDP for a chosen country.
        
        Args:
            country (str): The name of the country.
            years_ahead (int): Number of years to forecast.
            
        Returns:
            pd.DataFrame: A dataframe containing the forecast.
        """
        if self.model is None:
            raise FileNotFoundError("Model not loaded.")
            
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logging.error("Processed data file not found.")
            return pd.DataFrame()
            
        # Get the latest data for the specified country
        country_data = df[df['Country'] == country]
        if country_data.empty:
            logging.error(f"Country '{country}' not found in the dataset.")
            return pd.DataFrame()
            
        # Get the most recent row
        latest_row = country_data.sort_values('Year').iloc[-1]
        
        current_year = int(latest_row['Year'])
        current_gdp = latest_row['GDP_USD']
        
        forecasts = []
        
        # We need the previous year's GDP for the first prediction
        # To predict year N+1, we need Year=N+1, Previous_GDP=GDP_N, GDP_Diff=GDP_N - GDP_N-1...
        # Wait, the features for predicting year N+1 are based on what is known AT year N+1.
        # But at year N+1, Previous_GDP is GDP_N.
        # What is GDP_Difference for year N+1? It is GDP_N+1 - GDP_N. But we don't know GDP_N+1!
        # Ah, looking closely at the preprocess step:
        # df["GDP_Difference"] = df["GDP_USD"] - df["Previous_GDP"]
        # If the features to predict GDP_USD (target) are Year, Previous_GDP, GDP_Difference, GDP_Growth_Rate...
        # Then to predict GDP_USD at N+1, we need GDP_Difference at N+1.
        # But GDP_Difference at N+1 = GDP_USD at N+1 (which we are predicting!) - Previous_GDP (which is GDP_USD at N).
        # This means GDP_Difference and GDP_Growth_Rate are theoretically leaking the target!
        # However, following the spec strictly: "year N+1's prediction becomes year N+2's Previous_GDP / GDP_Difference / GDP_Growth_Rate inputs"
        # So we'll use the *previous* known difference and growth rate, or we have to calculate them based on the step.
        # The exact text says: "year N+1's prediction becomes year N+2's Previous_GDP / GDP_Difference / GDP_Growth_Rate inputs"
        # Let's interpret it as: when we predict for year T, we construct its features based on year T-1's state, but wait, the feature is for the *current* row.
        # Actually, let's just use the previous step's prediction to build the features for the next step.
        # For predicting year T:
        # Previous_GDP = prediction from T-1 (or actual from T-1 if T is the first forecast year)
        # We can't know GDP_Difference at T until we predict GDP at T. 
        # But since the spec requires us to feed them as inputs, we will calculate them from the *previous* step, effectively lagging them by one more year? 
        # No, if the features are Year, Previous_GDP, GDP_Difference, GDP_Growth_Rate, and the target is GDP_USD, 
        # during training, GDP_Difference = GDP_USD - Previous_GDP. 
        # This is a perfect colinearity / target leakage in training! 
        # GDP_USD = Previous_GDP + GDP_Difference. 
        # A linear regression will just learn coefficients (0, 1, 1, 0) and perfectly predict GDP_USD.
        # Well, the spec says "Features: Year, Previous_GDP, GDP_Difference, GDP_Growth_Rate -> Target: GDP_USD".
        # I must implement it exactly as specified.
        # For forecasting step T:
        # We will use the last known difference and growth rate as proxies if we must, 
        # OR we just use the difference between (prediction_T-1) and (prediction_T-2).
        
        prev_gdp = current_gdp
        prev_prev_gdp = latest_row['Previous_GDP']
        
        for i in range(1, years_ahead + 1):
            next_year = current_year + i
            
            # Construct features for next_year
            # Since we can't know the difference and growth rate for the year we are predicting, 
            # we will use the difference and growth from the PREVIOUS transition.
            # i.e., difference = prev_gdp - prev_prev_gdp
            diff = prev_gdp - prev_prev_gdp
            growth = diff / prev_prev_gdp if prev_prev_gdp != 0 else 0
            
            features_df = pd.DataFrame([{
                "Year": next_year,
                "Previous_GDP": prev_gdp,
                "GDP_Difference": diff,
                "GDP_Growth_Rate": growth
            }])
            
            pred_gdp = self.model.predict(features_df[FEATURES])[0]
            
            forecasts.append({
                "Year": next_year,
                "Country": country,
                "Forecasted_GDP_USD": pred_gdp
            })
            
            # Shift variables for next iteration
            prev_prev_gdp = prev_gdp
            prev_gdp = pred_gdp
            
        return pd.DataFrame(forecasts)
        
    def run(self, country: str):
        """Execute and print the forecast."""
        print(f"--- 5-Year Forecast for {country} ---")
        df_forecast = self.forecast(country)
        if not df_forecast.empty:
            print(df_forecast.to_string(index=False))
        else:
            print("Forecast could not be generated.")

if __name__ == "__main__":
    forecaster = GDPForecaster()
    # Provide a default country for standalone testing
    if len(sys.argv) > 1:
        country_to_forecast = sys.argv[1]
    else:
        country_to_forecast = "India"
        
    if forecaster.model is not None:
        forecaster.run(country_to_forecast)
