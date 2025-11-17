"""
market.py
Defines the Market class
"""
import pandas as pd
import numpy as np

class Market:
    """
    Contains ALL time-series and meta data for assets, immutable
    """
    FIELD_LEVEL = "field"
    DATE_FIELD = "datetime"
    REQUIRED_FIELDS = ['open', 'high', 'low', 'close', 'volume']

    #============= CONSTRUCTORS ============
    def __init__(self, 
                 price_data : pd.DataFrame,
                 meta_data : pd.DataFrame = None,
                 fundemental_data : pd.DataFrame = None,
                 dividend_data : pd.DataFrame = None,
                 macro_data : pd.DataFrame = None,
                 fx_data : pd.DataFrame = None):
        
        self.price_data = price_data 
        self.dividend_data = dividend_data
        self.fundemental_data = fundemental_data
        self.meta_data = meta_data
        self.macro_data = macro_data
        self.fx_data = fx_data

        self._validate()

        self.cache = {} 
    
    @classmethod
    def from_csv(cls):
        pass

    @classmethod
    def from_alphavantage(cls):
        pass

    @classmethod
    def from_sql(cls):
        pass
    
    #================ PRIVATE METHODS =============
    def _validate(self):
        pass

    #================ PUBLIC APIs ============
    def price(self, ticker : str, field : str = "close") -> pd.DataFrame:
        """
        Return a time-series of price of a single ticker
        """
        if field not in self.REQUIRED_FIELDS:
            raise ValueError(f"Invalid field : {field}")
        if ticker not in self.price_data.columns.levels[0]:
            raise ValueError(f"Ticker {ticker} not found in price data")
        
        return self.price_data[ticker][field]
    
    def dividends(self, ticker : str) -> pd.Series:
        """
        Return a timeseries of dividends of a ticker
        """
        if self.dividend_data is None:
            raise ValueError("Dividend data was never defined")
        if ticker not in self.dividend_data.columns:
            raise ValueError(f"Unable to find ticker {ticker} in divdend data")
        
        return self.dividend_data[ticker]
    
    def fundemental(self, ticker : str, field : str) -> pd.Series:
        """
        Return a timeseries of a filed of a ticker
        """
        if self.fundemental_data is None:
            raise ValueError("Fundemental data was never defined")
        if ticker not in self.fundemental_data.columns.levels[0]:
            raise ValueError(f"Unable to find ticker {ticker} in fundemental data")
        if field not in self.fundemental_data[ticker].columns:
            raise ValueError(f"Unable to find field {field} in fundemental data")
        return self.fundemental_data[ticker][field]
        

    def tickers(self):
        """
        A list of tickers in each of the dataframes
        """
        return list(self.price_data.columns.columns.levels[0])


