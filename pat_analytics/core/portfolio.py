import pandas as pd
import datetime
import numpy as np

from .engine.simple import SimpleBacktester

class Portfolio:
    """
    Main way users interact with pat_analytics  
    Given cleaned market data, performs portfolio computations
    """

    FIELD_LEVEL = "field"
    REQUIRED_FIELDS = ['open', 'high', 'low', 'close', 'volume']
    BACKTESTERS = {
        "simple" : SimpleBacktester
    }

    def __init__(self, pxaction : pd.DataFrame, metadata : pd.DataFrame,  
                 weight : pd.Series = None, rebalance_period : str = "none"):
        """
        Cannonical constructor. Expects a Multiindexed Dataframe

        pxaction        : MultiIndex Dataframe [(ticker, type) x time] -> price (dollar amount)
        metadata        : Dataframe [data_type x ticker] -> value (sector, 2023Q1 earnings, country, currency etc)
        weight          : Series [ticker] -> weight (must add up to 1), if None then metadata must include 'amt_shares'
        rebalance_period: String for how often to rebalance the weights to original
        market_value    : If no share amount is given, get a starting market value of the portfolio

        The user is free to either give quantity of shares they own through the metadata table in a column named
        'quantity', or specify their starting weight through the weight Series.  
        """

        if not isinstance(pxaction, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        if not isinstance(pxaction.columns, pd.MultiIndex):
            raise ValueError("Data must have multiindex columns, if using dict try from_dict()")
        
        #normalize cols
        pxaction.columns = pd.MultiIndex.from_tuples(
            [(str(sym), str(field)) for sym, field in pxaction.columns],
            names=['ticker', self.FIELD_LEVEL]
        )

        self.pxaction : pd.DataFrame = pxaction.sort_index(axis=1)
        self.metadata : pd.DataFrame= metadata
        self.rebalance_period : pd.Timedelta = self._parse_rebalance_period(rebalance_period)

        #cache (have the slices ready)
        self._cache = {} 
        
        #starting weight and share quantity
        self.w0 , self.q0 = self._init_start_weight(weight)

        self.returns : pd.DataFrame = self.close.pct_change().fillna(0)

        # users must backtest for this value
        self.weight : pd.DataFrame = None 
        self.quantity : pd.DataFrame = None

    def _field(self, name : str) -> pd.DataFrame:
        """
        For caching slices, and easy access to just close, open etc
        """
        if name not in self._cache:
            self._cache[name] = self.pxaction.xs(name, axis=1, level=self.FIELD_LEVEL)

        return self._cache[name]
    
    def clear_cache(self):
        """
        If pxaction df changes, easy to clear the cache
        """
        self._cache.clear() 
        
    @property
    def open(self) -> pd.DataFrame: return self._field("open")
    
    @property
    def high(self) -> pd.DataFrame: return self._field("high")
    
    @property
    def low(self) -> pd.DataFrame: return self._field("low")
    
    @property
    def close(self) -> pd.DataFrame: return self._field("close")
    
    @property
    def volume(self) -> pd.DataFrame: return self._field("volume")

    """
    UTILS
    """

    def _parse_rebalance_period(self, period : str | pd.Timedelta | int | float | None) -> pd.Timedelta:
        """
        Parses the rebalance period. Period can be a str ('1D', '15min', etc),
        an int to indicate days, or None to not rebalance at all.
        """
        if period == "none" or period is None:
            return None

        if isinstance(period, pd.Timedelta):
            return period
        
        if isinstance(period, (int, float)):
            return pd.to_timedelta(period, 'D')

        try:
            return pd.to_timedelta(period)
        except:
            raise ValueError(f"Invalid rebalance period '{period}'. Use eg \'1D\', \'15min\', \'30s\' or numeric days")
    
    def _init_start_weight(self, init_weight : pd.Series | None) -> tuple[pd.Series, pd.Series]:
        """
        If the user did not specify a weight, infer from share count in metadata. 
        If they specified a weight then infer the amount of shares
        """
        qty_col_name = 'quantity'
        default_market_value = 1.0

        has_qty = qty_col_name in self.metadata.columns
        has_weight = init_weight is not None

        if has_qty == has_weight:
            raise ValueError("Either specify quantity in metadata, or starting weight. Must have exactly one")
        
        price : pd.Series = self.close.iloc[0, :] # first price
        tickers = price.index.astype(str)

        #align, sanity check, number crunch, return
        if has_qty: #get weight
            quantity : pd.Series = self.metadata[qty_col_name].reindex(tickers).fillna(0)
            total_market_value : float = (quantity * price).sum()
            if total_market_value <= 0:
                raise ValueError("Market Value can not be zero!")
            weight : pd.Series = (quantity * price) / total_market_value
            return weight, quantity
        
        else: #get quantity
            init_weight = init_weight.reindex(tickers).fillna(0)
            if init_weight.sum() <= 0:
                raise ValueError("Weights must sum to a positive value!")
            init_weight /= init_weight.sum()
            quantity : pd.Series = (default_market_value * init_weight)  / price 
            return init_weight, quantity 

    
    """
    ALTERNATE CONSTRUCTORS
    """
    @classmethod
    def from_dict(cls, 
                  data_dict         : dict[str, pd.DataFrame | pd.Series],
                  metadata          : pd.DataFrame,
                  weight            : pd.Series = None,
                  rebalance_period  : str = "none"):
        """
        Init a Portfolio object using a dictonary. Dictionary is from ticker to 
        series or dataframe. 
        If only a series is passed for each, interpreted as only the close price
        Construct a multiindexed df to contain the data
        """
        frames = []

        for ticker, obj in data_dict.items():
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
            
            df.columns = pd.MultiIndex.from_product([[ticker]], df.columns)
            frames.append(df)
        
        data = pd.concat(frames, axis=1).sort_index(axis=1)

        return cls(data, metadata, weight, rebalance_period)
        
    """
    PUBLIC METHODS
    """
    def run_backtest(self, type : str = "simple", **kwargs) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run a backtest, evolving the portfolio with or without rebalancing and/or 
        fee structure
        """
        
        cls = self.BACKTESTERS.get(type)
        if cls is None:
            raise ValueError(f"No Backtester type : {type}")
        
        bt = cls(self, **kwargs)
        self.weight, self.quantity = bt.run()
        return self.weight, self.quantity
    
    def get_total_returns(self) -> pd.Series:
        """
        Returns the returns of the portfolio as percent change
        or as dollar amount, depending on the isDollar flag
        """

        returns, weights = self.returns.align(self.weight, join="inner", axis=1)

        #as net return per time frame, NOT GROSS
        return (returns * weights).sum(axis = 1)
        
    def get_market_value(self) -> pd.Series:
        """
        Recieve the market value of the portfolio in dollar amount
        """
        qty, price = self.quantity.align(self.close, join="inner", axis=1)
        
        return (qty * price).sum(axis=1)



