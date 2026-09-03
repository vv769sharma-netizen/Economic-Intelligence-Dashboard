"""
Streamlit dashboard for the Economic Intelligence project.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config import BASE_DIR, get_news_api_key
from src.forecast import GDPForecaster
from src.news_fetcher import NewsFetcher

# Page Config
st.set_page_config(page_title="Economic Intelligence Dashboard", layout="wide", page_icon="📈")

# Custom CSS — news card grid + general polish
st.markdown("""
<style>
    /* Hide deploy button */
    .stDeployButton {display:none;}

    /* News card styling */
    .news-card {
        background: #1e2130;
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 14px;
        transition: border-color 0.2s ease;
    }
    .news-card:hover {
        border-color: #4f72ff;
    }
    .news-card .news-source {
        font-size: 11px;
        font-weight: 700;
        color: #4f72ff;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .news-card .news-title {
        font-size: 15px;
        font-weight: 600;
        color: #e8ecf5;
        margin-bottom: 6px;
        line-height: 1.4;
    }
    .news-card .news-title a {
        color: #e8ecf5;
        text-decoration: none;
    }
    .news-card .news-title a:hover {
        color: #4f72ff;
    }
    .news-card .news-desc {
        font-size: 13px;
        color: #8a93b0;
        margin-bottom: 8px;
        line-height: 1.5;
    }
    .news-card .news-date {
        font-size: 11px;
        color: #565e7e;
    }
    .news-image {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .news-section-header {
        font-size: 22px;
        font-weight: 700;
        color: #e8ecf5;
        border-left: 4px solid #4f72ff;
        padding-left: 12px;
        margin-bottom: 16px;
    }
    .news-api-notice {
        background: #12192c;
        border: 1px dashed #2e3250;
        border-radius: 8px;
        padding: 16px;
        color: #8a93b0;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def format_currency(val):
    """Format a numeric GDP value as a human-readable currency string."""
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


def format_date(iso_date: str) -> str:
    """Convert ISO 8601 date string to human-readable format."""
    try:
        dt = datetime.strptime(iso_date[:10], "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return iso_date[:10] if iso_date else ""


def render_news_card(article: dict):
    """Render a single news article as an HTML card."""
    title = article.get("title", "No title")
    url = article.get("url", "#")
    description = article.get("description") or ""
    source = article.get("source", {}).get("name", "Unknown")
    published = format_date(article.get("publishedAt", ""))
    image_url = article.get("urlToImage")

    image_html = ""
    if image_url:
        image_html = f'<img src="{image_url}" class="news-image" onerror="this.style.display=\'none\'">'

    desc_html = f'<p class="news-desc">{description[:160]}{"..." if len(description) > 160 else ""}</p>' if description else ""

    card_html = f"""
    <div class="news-card">
        {image_html}
        <div class="news-source">{source}</div>
        <div class="news-title"><a href="{url}" target="_blank">{title}</a></div>
        {desc_html}
        <div class="news-date">📅 {published}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache the processed GDP data."""
    data_path = BASE_DIR / "data" / "processed" / "cleaned_gdp.csv"
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_data(ttl=1800)  # Cache news for 30 minutes to respect API rate limits
def fetch_global_news():
    """Cached wrapper for fetching global economic news."""
    api_key = get_news_api_key()
    fetcher = NewsFetcher(api_key)
    return fetcher.fetch_global_economic_news(page_size=6)


@st.cache_data(ttl=1800)  # Cache news for 30 minutes
def fetch_country_news(country: str):
    """Cached wrapper for fetching country-specific economic news."""
    api_key = get_news_api_key()
    fetcher = NewsFetcher(api_key)
    return fetcher.fetch_country_news(country, page_size=6)


# ---------------------------------------------------------------------------
# News Section renderer
# ---------------------------------------------------------------------------

def render_news_section(selected_country: str):
    """Render the full news section — global headlines + country-specific tab."""
    st.markdown("---")
    st.markdown('<div class="news-section-header">📰 Economic News</div>', unsafe_allow_html=True)

    api_key = get_news_api_key()
    if not api_key:
        st.markdown("""
        <div class="news-api-notice">
            <strong>📡 GNews API key not configured.</strong><br>
            To enable live news on Streamlit Cloud, get a free API key at
            <a href="https://gnews.io/" target="_blank">gnews.io</a>
            (100 requests/day free), then set it in your Streamlit Cloud Secrets:<br><br>
            <code>NEWS_API_KEY = "your_key_here"</code><br><br>
        </div>
        """, unsafe_allow_html=True)
        return

    tab_global, tab_country = st.tabs([
        "🌍 Global Economic Headlines",
        f"🏳️ {selected_country} News"
    ])

    with tab_global:
        with st.spinner("Loading global economic news..."):
            try:
                articles = fetch_global_news()
                
                if not articles:
                    st.info("No global economic news found right now. Try again shortly.")
                else:
                    # 3-column grid
                    cols = st.columns(3)
                    for i, article in enumerate(articles):
                        with cols[i % 3]:
                            render_news_card(article)
            except Exception as e:
                st.error(f"Failed to load global news. API Error: {e}")

    with tab_country:
        with st.spinner(f"Loading news for {selected_country}..."):
            try:
                country_articles = fetch_country_news(selected_country)
                
                if not country_articles:
                    st.info(f"No recent economic news found for **{selected_country}**. Try selecting a major economy or widen your search.")
                else:
                    cols = st.columns(3)
                    for i, article in enumerate(country_articles):
                        with cols[i % 3]:
                            render_news_card(article)
            except Exception as e:
                st.error(f"Failed to load country news. API Error: {e}")


# ---------------------------------------------------------------------------
# Main Dashboard
# ---------------------------------------------------------------------------

def main():
    """Main Streamlit app entry point."""
    st.title("📈 Economic Intelligence Dashboard")

    df = load_data()

    if df.empty:
        st.error("Data not found. Please run the data extraction and preprocessing pipelines first.")
        st.stop()

    # ---- Sidebar ----
    st.sidebar.header("Filters")
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("Select a Country", countries)

    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    selected_years = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # ---- Filter Data ----
    country_df = df[
        (df['Country'] == selected_country) &
        (df['Year'] >= selected_years[0]) &
        (df['Year'] <= selected_years[1])
    ].copy()

    if country_df.empty:
        st.warning(f"No data available for {selected_country} in the selected year range.")
        st.stop()

    # ---- Metrics ----
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

    # ---- GDP Charts ----
    st.subheader(f"GDP Trend & Growth Rate — {selected_country}")
    fig_gdp = px.line(country_df, x='Year', y='GDP_USD', title="GDP over Time", markers=True)
    fig_growth = px.line(country_df, x='Year', y='GDP_Growth_Rate', title="GDP Growth Rate over Time", markers=True)
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(fig_gdp, width='stretch')
    with chart_col2:
        st.plotly_chart(fig_growth, width='stretch')

    # ---- Multi-Country Comparison ----
    st.subheader("Multi-Country Comparison")
    default_compare = ["India", "China", "United States"]
    default_selection = [c for c in default_compare if c in countries]
    selected_compare_countries = st.multiselect("Select Countries to Compare", countries, default=default_selection)
    if selected_compare_countries:
        compare_df = df[
            (df['Country'].isin(selected_compare_countries)) &
            (df['Year'] >= selected_years[0]) &
            (df['Year'] <= selected_years[1])
        ]
        fig_compare = px.line(compare_df, x='Year', y='GDP_USD', color='Country',
                              title="GDP Comparison over Time", markers=True)
        st.plotly_chart(fig_compare, width='stretch')
    else:
        st.info("Select at least one country to view the comparison chart.")

    # ---- Global GDP Map ----
    st.subheader("Global GDP Map")
    map_year = st.selectbox("Select Year for Map", sorted(df['Year'].unique(), reverse=True))
    map_df = df[df['Year'] == map_year]
    fig_map = px.choropleth(
        map_df, locations="Country_Code", color="GDP_USD",
        hover_name="Country", locationmode="ISO-3",
        title=f"Global GDP in {map_year}"
    )
    st.plotly_chart(fig_map, width='stretch')

    # ---- 5-Year Forecast ----
    st.subheader("5-Year GDP Forecast")
    try:
        forecaster = GDPForecaster()
        if forecaster.model is not None:
            forecast_df = forecaster.forecast(selected_country)
            if not forecast_df.empty:
                display_df = forecast_df.copy()
                display_df['Forecasted_GDP_USD'] = display_df['Forecasted_GDP_USD'].apply(format_currency)
                st.table(display_df)
                forecast_csv = forecast_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Download {selected_country} Forecast as CSV",
                    data=forecast_csv,
                    file_name=f"{selected_country}_gdp_forecast.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Could not generate forecast.")
        else:
            st.info("Forecasting model not found. Please run the training pipeline first.")
    except Exception as e:
        st.error(f"An error occurred while generating the forecast: {e}")

    # ---- Download Historical Data ----
    st.subheader("Download Historical Data")
    csv_data = country_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {selected_country} GDP Data as CSV",
        data=csv_data,
        file_name=f"{selected_country}_gdp_data.csv",
        mime="text/csv"
    )

    # ---- News Section (always last) ----
    render_news_section(selected_country)


if __name__ == "__main__":
    main()
