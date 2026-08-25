"""
Module for fetching economic news from NewsAPI.

Uses the free tier of NewsAPI (https://newsapi.org).
Free tier allows 100 requests/day. Results are cached in Streamlit
to avoid hammering the rate limit on every page rerun.
"""

import logging
import requests
from datetime import datetime, timedelta
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
NEWSAPI_TOP_ENDPOINT = "https://newsapi.org/v2/top-headlines"


class NewsFetcher:
    """Fetches economic and country-specific news from NewsAPI."""

    def __init__(self, api_key: str):
        """
        Initialize the fetcher with a NewsAPI key.

        Args:
            api_key (str): Your NewsAPI key. Get one free at https://newsapi.org/register
        """
        self.api_key = api_key
        self.timeout = 10

    def _is_configured(self) -> bool:
        """Check if a valid API key has been provided."""
        return bool(self.api_key and self.api_key.strip())

    def fetch_global_economic_news(self, page_size: int = 6) -> List[Dict]:
        """
        Fetch top global economic and financial news headlines.

        Args:
            page_size (int): Number of articles to return (max 100).

        Returns:
            List[Dict]: List of article dicts with keys: title, description,
                        url, urlToImage, publishedAt, source.
        """
        if not self._is_configured():
            logging.warning("NewsAPI key not configured. Returning empty news list.")
            return []

        # Search last 7 days for broad economic news
        from_date = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

        params = {
            "q": "economy OR GDP OR inflation OR \"economic growth\" OR \"world bank\" OR \"IMF\"",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "from": from_date,
            "apiKey": self.api_key,
        }

        try:
            response = requests.get(NEWSAPI_ENDPOINT, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            return [a for a in articles if a.get("title") and a["title"] != "[Removed]"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch global economic news: {e}")
            return []
        except ValueError as e:
            logging.error(f"Failed to parse NewsAPI JSON response: {e}")
            return []

    def fetch_country_news(self, country: str, page_size: int = 6) -> List[Dict]:
        """
        Fetch recent economic news specific to a given country.

        Args:
            country (str): Country name (e.g., "India", "United States").
            page_size (int): Number of articles to return (max 100).

        Returns:
            List[Dict]: List of article dicts.
        """
        if not self._is_configured():
            logging.warning("NewsAPI key not configured. Returning empty news list.")
            return []

        from_date = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")

        params = {
            "q": f'"{country}" AND (economy OR GDP OR inflation OR trade OR budget OR "economic")',
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "from": from_date,
            "apiKey": self.api_key,
        }

        try:
            response = requests.get(NEWSAPI_ENDPOINT, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            articles = data.get("articles", [])
            return [a for a in articles if a.get("title") and a["title"] != "[Removed]"]
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch news for {country}: {e}")
            return []
        except ValueError as e:
            logging.error(f"Failed to parse NewsAPI JSON response: {e}")
            return []
