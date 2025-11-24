"""
market.py
Defines the Market class
"""
import pandas as pd
import numpy as np

from datetime import datetime

from pat_analytics.utils.utils import add_column_multiidx
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
        """
        Canonical constructor for the Market Object
        price_data          : MultiIndex Dataframe [(ticker, type) x time] -> price (dollar amount)
        meta_data           : Dataframe [ticker x data_type] -> value (sector, country, currency etc)
        fundemental_data    : MultiIndex DataFrame [(ticker, type) x time] -> value () 
        dividend_data       : DataFrame [ticker x time] -> dividend yield
        macro_data          : DataFrame [t-bill type x time] -> yield
        fx_data             : DataFrame [currency x time] -> price (1 Currency price in USD)
        """
        
        self.price_data = price_data 
        self.dividend_data = dividend_data
        self.fundemental_data = fundemental_data
        self.meta_data = meta_data
        self.macro_data = macro_data
        self.fx_data = fx_data

        self._validate_and_clean()

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
    
    @classmethod
    def from_dict(cls, 
                  price_dict        : dict[str, pd.DataFrame | pd.Series],
                  meta_data         : pd.DataFrame = None,
                  fundemental_dict  : dict[str, pd.DataFrame] = None,
                  dividend_data     : pd.DataFrame = None,
                  macro_data        : pd.DataFrame = None,
                  fx_data           : pd.DataFrame = None
    ):
        """
        Init a Portfolio object using a dictonary. Dictionary is from ticker to 
        series or dataframe. 
        If only a series is passed for each, interpreted as only the close price
        Construct a multiindexed df to contain the data
        """
        frames = []

        for ticker, obj in price_dict.items():
            obj.index = obj[cls.DATE_FIELD]
            if isinstance(obj, pd.Series): #close only
                df = pd.DataFrame(index=obj.index)
                for f in cls.REQUIRED_FIELDS:
                    df[f] = obj if f == 'close' else np.nan

            elif isinstance(obj, pd.DataFrame): #more than just close
                df = obj.copy()
                for f in cls.REQUIRED_FIELDS:
                    if f not in df.columns:
                        df[f] = np.nan
                
                df = df[cls.REQUIRED_FIELDS]

            else:
                raise TypeError(f"Unsuported type for {ticker} : {type(obj)}")
            
            df.columns = pd.MultiIndex.from_product([[ticker], df.columns] )
            frames.append(df)
        
        data = pd.concat(frames, axis=1).sort_index(axis=1)


        return cls(data, meta_data)

    #================ PRIVATE METHODS =============
    def _validate_and_clean(self):
        """
        Validates and Cleans input
        """
        if not isinstance(self.price_data, pd.DataFrame):
            raise TypeError("Price data must be a pandas DataFrame")
        if not isinstance(self.price_data.columns, pd.MultiIndex):
            raise TypeError("Price data must have multiindex columns, if using dict try from_dict()")
        
        if self.dividend_data is not None and not isinstance(self.dividend_data, pd.DataFrame):
            raise TypeError("Dividend data must be a pandas DataFrame")
        
        if self.fundemental_data is not None:
            if not isinstance(self.fundemental_data, pd.DataFrame):
                raise TypeError("Fundemental Data must be a pandas DataFrame")
            if not isinstance(self.fundemental_data.columns, pd.MultiIndex):
                raise TypeError("Fundemental data must have multiindex columns")
        
        if self.meta_data is not None and not isinstance(self.meta_data, pd.DataFrame):
            raise TypeError("Meta Data must be a pandas DataFrame")
        
        if self.macro_data is not None and not isinstance(self.macro_data, pd.DataFrame):
            raise TypeError("Macro Data must be a dataframe")
        
        if self.fx_data is not None:
            if not isinstance(self.fx_data, pd.DataFrame):
                raise TypeError("FX Data must be a pandas DataFrame")
            if not isinstance(self.fx_data.columns, pd.MultiIndex):
                raise TypeError("FX Data must have multiindex columns")
        
        #ensure the indexes are datetimes, sorted in descending order
        if not self.price_data.index.inferred_type == "datetime64":
            raise TypeError("Indexes of price data must be datetime64 objects")
        
        self.price_data = self.price_data.sort_index()

        # TODO do the above for the rest of the dfs

        #create a fake position called 'CASH' to keep track of the users cash
        self.price_data = add_column_multiidx(self.price_data, "CASH", 1)
        
    #================ PUBLIC APIs ============
    def price(self, ticker : str = "universe" , field : str = "close") -> pd.DataFrame:
        """
        Return a time-series of price of a single ticker or multiple tickers,
        if not given a ticker or passed a ticker 'universe' pass the entire dataframe
        """
        if field not in self.REQUIRED_FIELDS:
            raise ValueError(f"Invalid field : {field}")
        
        if ticker == 'universe':
            return self.price_data.xs('close', axis=1, level=1)
        
        #normalize
        if isinstance(ticker, str):
            tickers = [ticker]
        elif isinstance(ticker, (list, tuple, set)):
            tickers = list(ticker)
        else:
            raise TypeError("Tickers must of type str or a list/tupple/set of strings")
        
        missing = [t for t in tickers if t not in self.price_data.columns.levels[0]]
        if missing: 
            raise ValueError(f"Tickers not found in price data {missing}")
        
        df = self.price_data[tickers][field]

        #make sure output is a dataframe
        return df if isinstance(df, pd.DataFrame) else df.to_frame()
    
    #TODO: make the rest allowed for lists of tickers as well
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
    
    def up_to(self, time : datetime):
        """
        Returns a slice of the market up to time t
        """
        price_slice = self.price_data.loc[:time].copy()

        div_slice = None
        if self.dividend_data is not None:
            div_slice = self.dividend_data.loc[:time].copy()

        fund_slice = None
        if self.fundemental_data is not None:
            fund_slice = self.fundemental_data.loc[:time].copy()   

        macro_slice = None
        if self.macro_data is not None:
            macro_slice = self.macro_data.loc[:time].copy()
        
        fx_slice = None
        if self.fx_data is not None:
            fx_slice = self.fx_data.loc[:time].copy()
        
        return Market(price_data=price_slice,
                      meta_data=self.meta_data,
                      fundemental_data=fund_slice,
                      dividend_data=div_slice,
                      macro_data=macro_slice,
                      fx_data=fx_slice)
    
    @property
    def tickers(self):
        """
        A list of tickers in each of the dataframes
        """
        return list(self.price_data.columns.levels[0])


