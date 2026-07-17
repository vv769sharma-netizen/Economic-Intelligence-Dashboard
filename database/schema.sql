CREATE DATABASE IF NOT EXISTS economic_dashboard;
USE economic_dashboard;

CREATE TABLE IF NOT EXISTS gdp_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255) NOT NULL,
    country_code VARCHAR(10),
    year INT NOT NULL,
    gdp_usd DOUBLE,
    previous_gdp DOUBLE,
    gdp_difference DOUBLE,
    gdp_growth_rate DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_country_year (country, year)
);
