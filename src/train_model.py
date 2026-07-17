"""
Module for training the GDP forecasting model.
"""

import sys
import logging
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from config import BASE_DIR, MODEL_PATH, FEATURES, TARGET

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ModelTrainer:
    """Class to train and save the GDP forecasting model."""
    
    def __init__(self):
        """Initialize paths and configuration."""
        self.input_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
        
    def train(self):
        """Train the model and save it."""
        logging.info(f"Loading data from {self.input_path}")
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logging.error(f"Input file {self.input_path} not found.")
            sys.exit(1)
            
        # Ensure we have the required columns
        missing_cols = [col for col in FEATURES + [TARGET] if col not in df.columns]
        if missing_cols:
            logging.error(f"Missing required columns in dataset: {missing_cols}")
            sys.exit(1)
            
        # Drop rows with NaN in features or target
        df = df.dropna(subset=FEATURES + [TARGET])
        
        X = df[FEATURES]
        y = df[TARGET]
        
        logging.info("Splitting data into train/test sets (80/20)...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        logging.info("Training Linear Regression model...")
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        logging.info("Evaluating model...")
        y_pred = model.predict(X_test)
        
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        
        print("="*40)
        print("MODEL EVALUATION")
        print("="*40)
        print(f"R² Score: {r2:.4f}")
        print(f"MAE:      {mae:,.2f}")
        print(f"RMSE:     {rmse:,.2f}")
        print("="*40)
        
        if r2 < 0:
            logging.warning("WARNING: R² score is negative! The model is performing worse than a horizontal line.")
            
        logging.info(f"Saving model to {MODEL_PATH}")
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        logging.info("Model saved successfully.")

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train()
