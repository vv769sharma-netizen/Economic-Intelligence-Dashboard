# Graph Report - .  (2026-08-26)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 101 nodes · 120 edges · 11 communities (9 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ed32dae`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.py
- Community 1
- NewsFetcher
- GDPDataExtractor
- GDPForecaster
- GDPPreprocessor
- config.py
- ModelTrainer
- EDAGenerator
- __init__.py
- __init__.py

## God Nodes (most connected - your core abstractions)
1. `NewsFetcher` - 9 edges
2. `DatabaseConnection` - 6 edges
3. `GDPDataExtractor` - 6 edges
4. `render_news_section()` - 6 edges
5. `GDPForecaster` - 5 edges
6. `DatabaseLoader` - 5 edges
7. `GDPPreprocessor` - 5 edges
8. `main()` - 5 edges
9. `EDAGenerator` - 4 edges
10. `ModelTrainer` - 4 edges

## Surprising Connections (you probably didn't know these)
- `DatabaseLoader` --uses--> `DatabaseConnection`  [INFERRED]
  src/load_database.py → database/db_connection.py
- `fetch_global_news()` --calls--> `NewsFetcher`  [EXTRACTED]
  app.py → src/news_fetcher.py
- `fetch_country_news()` --calls--> `NewsFetcher`  [EXTRACTED]
  app.py → src/news_fetcher.py

## Import Cycles
- None detected.

## Communities (11 total, 2 thin omitted)

### Community 0 - "app.py"
Cohesion: 0.16
Nodes (17): fetch_country_news(), fetch_global_news(), format_currency(), format_date(), load_data(), main(), Streamlit dashboard for the Economic Intelligence project., Convert ISO 8601 date string to human-readable format. (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.20
Nodes (8): DatabaseConnection, Manages the SQLAlchemy database connection., Returns a cached SQLAlchemy engine.                  Returns:             Engine, Test the database connection with a simple SELECT 1., Engine, DatabaseLoader, Class to handle loading data into the database., Execute the loading process.

### Community 2 - "NewsFetcher"
Cohesion: 0.20
Nodes (7): NewsFetcher, Module for fetching economic news from NewsAPI.  Uses the free tier of NewsAPI (, Fetches economic and country-specific news from NewsAPI., Initialize the fetcher with a NewsAPI key.          Args:             api_key (s, Check if a valid API key has been provided., Fetch top global economic and financial news headlines.          Args:, Fetch recent economic news specific to a given country.          Args:

### Community 3 - "GDPDataExtractor"
Cohesion: 0.22
Nodes (7): GDPDataExtractor, DataFrame, Class to extract and process raw GDP data from the World Bank API., Initialize the extractor with the API URL and output path., Fetch data from the API.                  Returns:             list: The records, Convert raw records to a DataFrame, keeping only necessary columns and dropping, Execute the extraction pipeline and save to CSV.

### Community 4 - "GDPForecaster"
Cohesion: 0.20
Nodes (7): GDPForecaster, DataFrame, Module for forecasting GDP for a chosen country iteratively., Execute and print the forecast., Class to forecast future GDP iteratively., Initialize and load the model., Forecast GDP for a chosen country.                  Args:             country (s

### Community 5 - "GDPPreprocessor"
Cohesion: 0.20
Nodes (7): GDPPreprocessor, DataFrame, Module for preprocessing raw GDP data., Class to clean and preprocess raw GDP data., Initialize paths for input and output., Run the preprocessing pipeline.                  Returns:             pd.DataFra, Execute the preprocessing and save the result.

### Community 6 - "config.py"
Cohesion: 0.25
Nodes (4): Module for managing database connections., Module for Exploratory Data Analysis (EDA) on GDP data., Module for extracting GDP data from the World Bank API., Module to load processed GDP data into the MySQL database.

### Community 7 - "ModelTrainer"
Cohesion: 0.25
Nodes (5): ModelTrainer, Module for training the GDP forecasting model., Class to train and save the GDP forecasting model., Initialize paths and configuration., Train the model and save it.

### Community 8 - "EDAGenerator"
Cohesion: 0.40
Nodes (3): EDAGenerator, Class to perform EDA and generate charts., Run EDA and generate interactive charts.

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GDPDataExtractor` connect `GDPDataExtractor` to `config.py`?**
  _High betweenness centrality (0.179) - this node is a cross-community bridge._
- **Why does `NewsFetcher` connect `NewsFetcher` to `app.py`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._