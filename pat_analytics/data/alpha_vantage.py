import requests
import pandas as pd
import io
from datetime import date
from typing import Tuple, Optional

class AlphaVantageLoader:
    """
    Utility for collecting market information from AlphaVantage.
    """
    def __init__(self, api_key: str):
        self.base_url = "https://www.alphavantage.co/query?"
        self.api_key = api_key

    def _safe_get(self, params: dict, mode: str = 'csv') -> io.StringIO | dict:
        params['apikey'] = self.api_key
        params['datatype'] = mode
        
        response = requests.get(self.base_url, params=params, timeout=15)

        if response.status_code != 200:
            raise ConnectionError(f"HTTP {response.status_code}: {response.text}")

        if "Note" in response.text and mode == 'json':
            raise RuntimeWarning(f"AlphaVantage Notice: {response.json().get('Note')}")
        
        if "Error Message" in response.text:
            raise ValueError(f"API Error: {response.text}")

        return io.StringIO(response.text) if mode == 'csv' else response.json()

    def decompose_datetime(self, df: pd.DataFrame, date_col: str, inplace: bool = True) -> Optional[pd.DataFrame]:
        """
        Explodes a datetime column into components. 
        Note: Epoch conversion removed to prevent plotting errors.
        """
        if not inplace:
            df = df.copy()

        df[date_col] = pd.to_datetime(df[date_col])
        
        dt_s = df[date_col].dt
        df['year'] = dt_s.year
        df['month'] = dt_s.month
        df['day'] = dt_s.day
        df['hour'] = dt_s.hour
        df['minute'] = dt_s.minute
        # No more epoch!

        return df if not inplace else None

    def get_intraday_px(self, ticker: str, interval: str = '5min', month: str = None) -> pd.DataFrame:
        """
        Fetches intraday data and sets index to Datetime objects.
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": ticker,
            "interval": interval,
            "outputsize": "full"
        }
        if month:
            params['month'] = month

        csv_data = self._safe_get(params, mode='csv')
        
        content = csv_data.getvalue()
        if "timestamp" not in content.lower():
            raise ValueError(f"AlphaVantage Error: {content[:200]}")
            
        csv_data.seek(0)
        df = pd.read_csv(csv_data)
        
        # Convert to datetime and set as index
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        
        return df[['open', 'high', 'low', 'close', 'volume']]
    
    def get_daily_px(self, ticker: str, output_size: str = 'compact') -> pd.DataFrame:
        """
        Fetches daily data and sets index to Datetime objects.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "outputsize": output_size
        }

        csv_data = self._safe_get(params, mode='csv')
        
        content = csv_data.getvalue()
        if "timestamp" not in content.lower():
            raise ValueError(f"AlphaVantage Error: {content[:200]}")
            
        csv_data.seek(0)
        df = pd.read_csv(csv_data)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        
        return df[['open', 'high', 'low', 'close', 'volume']]

    def get_etf_profile(self, ticker: str) -> dict:
        params = {"function": "ETF_PROFILE", "symbol": ticker}
        data = self._safe_get(params, mode='json')
        
        holdings = pd.json_normalize(data.get('holdings', []))
        holdings = holdings.rename(columns={'symbol': 'ticker', 'description': 'name'})
        if not holdings.empty:
            holdings['weight'] = holdings['weight'].astype(float)

        return {
            "holdings": holdings,
            "div_yield": float(data.get('dividend_yield', 0)),
            "inception": data.get('inception_date'),
            "expense_ratio": float(data.get('net_expense_ratio', 0))
        }