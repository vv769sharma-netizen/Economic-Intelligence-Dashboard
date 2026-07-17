# Graph Report - .  (2026-07-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 77 nodes · 88 edges · 9 communities (7 shown, 2 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6c65998a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8

## God Nodes (most connected - your core abstractions)
1. `GDPForecaster` - 7 edges
2. `DatabaseConnection` - 6 edges
3. `GDPDataExtractor` - 6 edges
4. `DatabaseLoader` - 5 edges
5. `GDPPreprocessor` - 5 edges
6. `main()` - 4 edges
7. `EDAGenerator` - 4 edges
8. `ModelTrainer` - 4 edges
9. `load_data()` - 3 edges
10. `format_currency()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `DatabaseLoader` --uses--> `DatabaseConnection`  [INFERRED]
  src/load_database.py → database/db_connection.py
- `main()` --calls--> `GDPForecaster`  [EXTRACTED]
  app.py → src/forecast.py

## Import Cycles
- None detected.

## Communities (9 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (12): format_currency(), load_data(), main(), Streamlit dashboard for the Economic Intelligence project., Load and cache the processed data., GDPForecaster, DataFrame, Module for forecasting GDP for a chosen country iteratively. (+4 more)

### Community 1 - "Community 1"
Cohesion: 0.20
Nodes (8): DatabaseConnection, Manages the SQLAlchemy database connection., Returns a cached SQLAlchemy engine.                  Returns:             Engine, Test the database connection with a simple SELECT 1., Engine, DatabaseLoader, Class to handle loading data into the database., Execute the loading process.

### Community 2 - "Community 2"
Cohesion: 0.22
Nodes (7): GDPDataExtractor, DataFrame, Class to extract and process raw GDP data from the World Bank API., Initialize the extractor with the API URL and output path., Fetch data from the API.                  Returns:             list: The records, Convert raw records to a DataFrame, keeping only necessary columns and dropping, Execute the extraction pipeline and save to CSV.

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (7): GDPPreprocessor, DataFrame, Module for preprocessing raw GDP data., Class to clean and preprocess raw GDP data., Initialize paths for input and output., Run the preprocessing pipeline.                  Returns:             pd.DataFra, Execute the preprocessing and save the result.

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (4): Module for managing database connections., Module for Exploratory Data Analysis (EDA) on GDP data., Module for extracting GDP data from the World Bank API., Module to load processed GDP data into the MySQL database.

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (5): ModelTrainer, Module for training the GDP forecasting model., Class to train and save the GDP forecasting model., Initialize paths and configuration., Train the model and save it.

### Community 6 - "Community 6"
Cohesion: 0.40
Nodes (3): EDAGenerator, Class to perform EDA and generate charts., Run EDA and generate interactive charts.

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `GDPDataExtractor` connect `Community 2` to `Community 4`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._