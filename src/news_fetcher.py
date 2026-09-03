"""
Module for fetching economic news from GNews API.

Uses the free tier of GNews (https://gnews.io).
Free tier allows 100 requests/day and works on cloud deployments like Streamlit.
Results are cached in Streamlit to avoid hammering the rate limit on every page rerun.
"""

import logging
import requests
from datetime import datetime, timedelta
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GNEWS_ENDPOINT = "https://gnews.io/api/v4/search"
GNEWS_TOP_ENDPOINT = "https://gnews.io/api/v4/top-headlines"


class NewsFetcher:
    """Fetches economic and country-specific news from GNews API."""

    def __init__(self, api_key: str):
        """
        Initialize the fetcher with a GNews API key.

        Args:
            api_key (str): Your API key. Get one free at https://gnews.io/
        """
        self.api_key = api_key
        self.timeout = 10

    def _is_configured(self) -> bool:
        """Check if a valid API key has been provided."""
        return bool(self.api_key and self.api_key.strip())

    def _map_article(self, a: dict) -> dict:
        """Map GNews article format to the format expected by the app (which was designed for NewsAPI)."""
        return {
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "urlToImage": a.get("image"),  # GNews uses 'image' instead of 'urlToImage'
            "publishedAt": a.get("publishedAt"),
            "source": {"name": a.get("source", {}).get("name", "Unknown")}
        }

    def fetch_global_economic_news(self, page_size: int = 6) -> List[Dict]:
        """
        Fetch top global economic and financial news headlines.

        Args:
            page_size (int): Number of articles to return (max 10 for GNews free).

        Returns:
            List[Dict]: List of article dicts.
        """
        if not self._is_configured():
            logging.warning("GNews API key not configured. Returning empty news list.")
            return []

        # For global economy, we search for broad economic terms
        params = {
            "q": "economy OR GDP OR inflation OR \"economic growth\" OR \"world bank\" OR \"IMF\"",
            "lang": "en",
            "max": page_size,
            "apikey": self.api_key,
            "sortby": "publishedAt"
        }

        response = requests.get(GNEWS_ENDPOINT, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        return [self._map_article(a) for a in articles if a.get("title")]

    def fetch_country_news(self, country: str, page_size: int = 6) -> List[Dict]:
        """
        Fetch recent economic news specific to a given country.

        Args:
            country (str): Country name (e.g., "India", "United States").
            page_size (int): Number of articles to return.

        Returns:
            List[Dict]: List of article dicts.
        """
        if not self._is_configured():
            logging.warning("GNews API key not configured. Returning empty news list.")
            return []

        params = {
            "q": f'"{country}" AND (economy OR GDP OR inflation OR trade OR budget OR "economic")',
            "lang": "en",
            "max": page_size,
            "apikey": self.api_key,
            "sortby": "publishedAt"
        }

        response = requests.get(GNEWS_ENDPOINT, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        
        return [self._map_article(a) for a in articles if a.get("title")]
