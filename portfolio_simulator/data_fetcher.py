"""
Data Fetcher Module - Handles fetching and processing market data
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union


class DataFetcher:
    """
    Fetches and processes market data using yfinance
    """

    def __init__(self):
        """Initialize the DataFetcher"""
        self.data_cache = {}

    def fetch_historical_data(
        self,
        symbols: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        """
        Fetch historical price data for given symbols

        Args:
            symbols: Single ticker or list of tickers
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            period: Period to download (e.g., '1d', '5d', '1mo', '1y', '5y', 'max')
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

        Returns:
            DataFrame with historical data
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        # Create cache key
        cache_key = f"{'-'.join(symbols)}_{start_date}_{end_date}_{period}_{interval}"

        # Check cache
        if cache_key in self.data_cache:
            return self.data_cache[cache_key].copy()

        # Fetch data
        try:
            if start_date and end_date:
                data = yf.download(
                    symbols,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    progress=False
                )
            else:
                data = yf.download(
                    symbols,
                    period=period,
                    interval=interval,
                    progress=False
                )

            # Cache the data
            self.data_cache[cache_key] = data.copy()

            return data

        except Exception as e:
            raise ValueError(f"Error fetching data for {symbols}: {str(e)}")

    def get_price_data(
        self,
        symbols: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        Get adjusted closing prices for symbols

        Args:
            symbols: Single ticker or list of tickers
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            period: Period to download

        Returns:
            DataFrame with adjusted closing prices
        """
        data = self.fetch_historical_data(symbols, start_date, end_date, period)

        if isinstance(symbols, list) and len(symbols) > 1:
            # Multiple symbols
            if 'Adj Close' in data.columns:
                prices = data['Adj Close']
            else:
                prices = data['Close']
        else:
            # Single symbol
            if 'Adj Close' in data.columns:
                prices = data['Adj Close']
            else:
                prices = data['Close']

            # Convert to DataFrame if Series
            if isinstance(prices, pd.Series):
                symbol = symbols[0] if isinstance(symbols, list) else symbols
                prices = prices.to_frame(name=symbol)

        return prices.dropna()

    def get_returns(
        self,
        symbols: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y",
        return_type: str = "simple"
    ) -> pd.DataFrame:
        """
        Calculate returns for given symbols

        Args:
            symbols: Single ticker or list of tickers
            start_date: Start date
            end_date: End date
            period: Period to download
            return_type: 'simple' or 'log' returns

        Returns:
            DataFrame with returns
        """
        prices = self.get_price_data(symbols, start_date, end_date, period)

        if return_type == "log":
            returns = np.log(prices / prices.shift(1))
        else:
            returns = prices.pct_change()

        return returns.dropna()

    def get_ticker_info(self, symbol: str) -> Dict:
        """
        Get ticker information

        Args:
            symbol: Ticker symbol

        Returns:
            Dictionary with ticker info
        """
        try:
            ticker = yf.Ticker(symbol)
            return ticker.info
        except Exception as e:
            raise ValueError(f"Error fetching info for {symbol}: {str(e)}")

    def get_latest_price(self, symbol: str) -> float:
        """
        Get the latest price for a symbol

        Args:
            symbol: Ticker symbol

        Returns:
            Latest price
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            else:
                raise ValueError(f"No data available for {symbol}")
        except Exception as e:
            raise ValueError(f"Error fetching latest price for {symbol}: {str(e)}")

    def clear_cache(self):
        """Clear the data cache"""
        self.data_cache = {}
