# Economic Intelligence Dashboard

An end-to-end data science pipeline and dashboard that extracts GDP data from the World Bank API, cleans it, stores it in a MySQL database, performs exploratory data analysis (EDA), trains a Linear Regression model for forecasting, and displays everything in an interactive Streamlit application.

## Folder Structure

```
Economic-Intelligence-Dashboard/
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── database/
│   ├── __init__.py
│   ├── schema.sql
│   └── db_connection.py
│
├── src/
│   ├── __init__.py
│   ├── extract_data.py
│   ├── preprocess.py
│   ├── load_database.py
│   ├── eda.py
│   ├── train_model.py
│   ├── forecast.py
│   └── utils.py
│
├── models/
├── reports/
│   └── charts/
└── dashboard/
```

## Prerequisites

- Python 3.11+
- MySQL Server (8.0+)

## Environment Variables

For the application to connect to your MySQL instance, set the following environment variables (or modify the defaults in `config.py`). The values below are the ones used for the local throwaway testing environment:

```env
DB_HOST=127.0.0.1
DB_PORT=3307
DB_NAME=economic_dashboard
DB_USER=root
DB_PASSWORD=
```
*(If you used a different password or port, please update accordingly).*

## Setup Instructions

### Windows

1. **Clone/Navigate to the directory**:
   ```powershell
   cd Economic-Intelligence-Dashboard
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Initialize Database**:
   Log into your MySQL server as root and execute the schema script:
   ```powershell
   mysql -u root -p < database/schema.sql
   ```

### macOS/Linux

1. **Clone/Navigate to the directory**:
   ```bash
   cd Economic-Intelligence-Dashboard
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**:
   Log into your MySQL server as root and execute the schema script:
   ```bash
   mysql -u root -p < database/schema.sql
   ```

## Running the Pipeline End-to-End

Execute the following commands in order from the project root:

1. **Extract Data**: Downloads raw JSON from the World Bank API and saves it to `data/raw/gdp_data.csv`.
   ```bash
   python src/extract_data.py
   ```

2. **Preprocess Data**: Cleans data, engineers lag and growth rate features, and saves to `data/processed/cleaned_gdp.csv`.
   ```bash
   python src/preprocess.py
   ```

3. **Load Database**: Truncates the `gdp_data` table and idempotently inserts the cleaned data. (Ensure your MySQL server is running and `config.py` has the right credentials).
   ```bash
   python src/load_database.py
   ```

4. **Exploratory Data Analysis (EDA)**: Generates dataset summaries and saves interactive Plotly charts to `reports/charts/`.
   ```bash
   python src/eda.py
   ```

5. **Train Model**: Trains a Linear Regression forecasting model and saves it to `models/gdp_forecast.pkl`.
   ```bash
   python src/train_model.py
   ```

6. **Test Forecast (Optional)**: Standalone test to print a 5-year iterative forecast for a specific country (e.g., India).
   ```bash
   python src/forecast.py India
   ```

7. **Launch Dashboard**: Start the Streamlit application to explore the data, charts, and forecasts interactively.
   ```bash
   streamlit run app.py
   ```
