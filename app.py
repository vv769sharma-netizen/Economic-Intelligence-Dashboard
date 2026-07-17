"""
Streamlit dashboard for the Economic Intelligence project.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from config import BASE_DIR
from src.forecast import GDPForecaster

# Page Config
st.set_page_config(page_title="Economic Intelligence Dashboard", layout="wide")

# Helper to format large numbers
def format_currency(val):
    if pd.isna(val):
        return "N/A"
    if val >= 1e12:
        return f"${val / 1e12:.2f}T"
    elif val >= 1e9:
        return f"${val / 1e9:.2f}B"
    elif val >= 1e6:
        return f"${val / 1e6:.2f}M"
    else:
        return f"${val:,.0f}"

@st.cache_data
def load_data():
    """Load and cache the processed data."""
    data_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
    try:
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def main():
    st.title("Economic Intelligence Dashboard")
    
    df = load_data()
    
    if df.empty:
        st.error("Data not found. Please run the data extraction and preprocessing pipelines first.")
        st.stop()
        
    # Sidebar
    st.sidebar.header("Filters")
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("Select a Country", countries)
    
    # Filter Data
    country_df = df[df['Country'] == selected_country].copy()
    
    if country_df.empty:
        st.warning(f"No data available for {selected_country}.")
        st.stop()
        
    # Metrics
    latest_row = country_df.sort_values('Year').iloc[-1]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Latest GDP", format_currency(latest_row['GDP_USD']))
    with col2:
        st.metric("Average GDP", format_currency(country_df['GDP_USD'].mean()))
    with col3:
        st.metric("Max GDP", format_currency(country_df['GDP_USD'].max()))
    with col4:
        st.metric("Min GDP", format_currency(country_df['GDP_USD'].min()))
        
    # Charts
    st.subheader(f"GDP Trend & Growth Rate for {selected_country}")
    
    fig_gdp = px.line(country_df, x='Year', y='GDP_USD', title="GDP over Time", markers=True)
    fig_growth = px.line(country_df, x='Year', y='GDP_Growth_Rate', title="GDP Growth Rate over Time", markers=True)
    
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(fig_gdp, use_container_width=True)
    with chart_col2:
        st.plotly_chart(fig_growth, use_container_width=True)
        
    # Forecast
    st.subheader("5-Year Forecast")
    
    try:
        forecaster = GDPForecaster()
        if forecaster.model is not None:
            forecast_df = forecaster.forecast(selected_country)
            if not forecast_df.empty:
                # Format the forecast for display
                display_df = forecast_df.copy()
                display_df['Forecasted_GDP_USD'] = display_df['Forecasted_GDP_USD'].apply(format_currency)
                st.table(display_df)
            else:
                st.warning("Could not generate forecast.")
        else:
            st.info("Forecasting model not found. Please run the training pipeline first to view forecasts.")
    except Exception as e:
        st.error(f"An error occurred while generating the forecast: {e}")
        
    # Download Button
    st.subheader("Download Data")
    csv_data = country_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {selected_country} Data as CSV",
        data=csv_data,
        file_name=f"{selected_country}_gdp_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
