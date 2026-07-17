"""
Module for Exploratory Data Analysis (EDA) on GDP data.
"""

import sys
import logging
import pandas as pd
import plotly.express as px
from config import BASE_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class EDAGenerator:
    """Class to perform EDA and generate charts."""
    
    def __init__(self):
        """Initialize paths."""
        self.input_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
        self.charts_dir = BASE_DIR / "reports" / "charts"
        
    def generate_eda(self):
        """Run EDA and generate interactive charts."""
        logging.info(f"Loading data from {self.input_path}")
        try:
            df = pd.read_csv(self.input_path)
        except FileNotFoundError:
            logging.error(f"Input file {self.input_path} not found.")
            sys.exit(1)
            
        # Summary statistics
        print("="*50)
        print("DATASET SUMMARY")
        print("="*50)
        print(f"Shape: {df.shape}")
        print(f"Number of countries: {df['Country'].nunique()}")
        print(f"Year range: {df['Year'].min()} to {df['Year'].max()}")
        print("\nGDP_USD Describe:")
        print(df['GDP_USD'].describe())
        print("="*50)
        
        # 1. Top-10 economies bar chart for the most recent year
        recent_year = df['Year'].max()
        df_recent = df[df['Year'] == recent_year].nlargest(10, 'GDP_USD')
        fig1 = px.bar(
            df_recent, x='Country', y='GDP_USD', 
            title=f"Top 10 Economies in {recent_year}",
            labels={'GDP_USD': 'GDP (USD)'},
            color='GDP_USD',
            color_continuous_scale='Viridis'
        )
        fig1_path = self.charts_dir / "top_10_economies.html"
        fig1.write_html(fig1_path)
        logging.info(f"Saved Top 10 economies chart to {fig1_path}")
        
        # 2. India GDP trend line chart
        df_india = df[df['Country'] == 'India']
        if not df_india.empty:
            fig2 = px.line(
                df_india, x='Year', y='GDP_USD',
                title="India GDP Trend",
                labels={'GDP_USD': 'GDP (USD)'},
                markers=True
            )
            fig2_path = self.charts_dir / "india_gdp_trend.html"
            fig2.write_html(fig2_path)
            logging.info(f"Saved India GDP trend chart to {fig2_path}")
        else:
            logging.warning("No data found for India. Skipping chart.")
            
        # 3. India vs China vs USA comparison line chart
        countries_to_compare = ['India', 'China', 'United States']
        df_compare = df[df['Country'].isin(countries_to_compare)]
        if not df_compare.empty:
            fig3 = px.line(
                df_compare, x='Year', y='GDP_USD', color='Country',
                title="GDP Comparison: India vs China vs USA",
                labels={'GDP_USD': 'GDP (USD)'},
                markers=True
            )
            fig3_path = self.charts_dir / "gdp_comparison.html"
            fig3.write_html(fig3_path)
            logging.info(f"Saved GDP comparison chart to {fig3_path}")
        else:
            logging.warning("Data for India/China/USA not found. Skipping chart.")

if __name__ == "__main__":
    eda = EDAGenerator()
    eda.generate_eda()
