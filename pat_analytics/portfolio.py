import pandas as pd
from typing import Dict
import datetime
import numpy as np

class Portfolio:
    """
    Main way users interact with pat_analytics  
    Given cleaned market data, performs portfolio computations
    """
    def __init__(self, pxaction : pd.DataFrame, metadata : pd.DataFrame,  
                 weight : pd.Series = None, rebalance_period : str = "none"):
        """
        pxaction       : Dataframe [ticker x time] -> price (dollar amount)
        metadata        : Dataframe [data_type x ticker] -> value (sector, 2023Q1 earnings, country, currency etc)
        weight          : Series [ticker] -> weight (must add up to 1), if None then metadata must include 'amt_shares'
        rebalance_period: String for how often to rebalance the weights to original
        market_value    : If no share amount is given, get a starting market value of the portfolio

        The user is free to either give quantity of shares they own throught the metadata table in a column named
        'quantity', or specify their starting weight through the weight Series.  
        """

        self.pxaction : pd.DataFrame = pxaction
        self.metadata : pd.DataFrame= metadata
        
        self.starting_weight , self.quantity = self._init_start_weight(weight)

        self.returns : pd.DataFrame = self.pxaction.pct_change().dropna()
        self.rebalance_period : pd.Timedelta = self._parse_rebalance_period(rebalance_period)
        self.weight : pd.DataFrame = self._init_weight_df(self)

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
        default_market_value = 1

        if not(qty_col_name in self.metadata ^ init_weight is None):
            raise ValueError("Either specify quantity in metadata, or starting weight. Must have exactly one")
        
        price : pd.Series = self.pxaction.iloc[0] # first price

        if qty_col_name in self.metadata: #get weight

            quantity : pd.Series = self.metadata[qty_col_name]
            total_market_value : float = (quantity @ price).sum()
            weight : pd.Series = (quantity @ price) / total_market_value

            return weight, quantity
        
        elif init_weight is None: #get quantity
            quantity : pd.Series = (default_market_value * init_weight) @ (1 / price)  
            return init_weight, quantity 

    
    def _init_weight_df(self):
        """
        Initializes the weight dataframe based on the 
        rebalancing period and pxaction
        """
        
        
        
    
    def get_total_returns(self, isDollar : bool = False):
        """
        Returns the returns of the portfolio as percent change
        or as dollar amount, depending on the isDollar flag
        """
        
    def get_market_value(self, time : datetime.datetime = None) -> np.float64:
        """
        Recieve the market value of the portfolio in dollar amount
        at time, if None then latest date in df
        """
        if time is None:
            time = self.pxaction.index[-1]

        return self.pxaction[time]




