"""
portfolio.py

Defines the Portfolio class
"""
import pandas as pd
from datetime import datetime

from pat_analytics import Market

class Portfolio:
    """
    Portfolio class contains all information 
    regarding a portfolio
    """
    def __init__(self,
                 market : Market,
                 init_weight : pd.Series | str = None, 
                 init_quantity : pd.Series = None, 
                 init_market_value : float = 1.0):
        """
        Canonical constructor of portfolio
        market              : Market (Market object)
        init_weight         : pd.Series [ticker] -> weight  | str (the weight of each position in the portfolio at the start)
        init_quantity       : pd.Series [ticker] -> quantity of stock (the quantity of each position in the portfolio at the start)
        init_market_value   : float (the starting market value of the portfolio in USD)
        User must provide either weight or quantity
        """
        self.market = market
        self.mv0 = init_market_value
        self.w0, self.q0 = self._init_start_weight(init_weight, init_quantity)
    

        self.weight : pd.DataFrame = None
        self.quantity : pd.DataFrame = None

        self._returns : pd.Series = None 

        self._validate()

    def _validate(self):
        """
        Validates input
        """
        pass

    def up_to(self, time : datetime):
        """
        Returns a copy of the portfolio
        but up to time t
        """
        new_port = Portfolio(self.market, init_weight=self.w0, init_market_value=self.mv0)

        if self.weight is not None:
            new_port.weight = self.weight.loc[:time].copy()
        
        if self.quantity is not None:
            new_port.quantity = self.quantity.loc[:time].copy()
        
        return new_port

    def _init_start_weight(self, 
                           init_weight : pd.Series | None,
                           init_quantity : pd.Series | None
                           ) -> tuple[pd.Series, pd.Series]:
        """
        If the user did not specify a weight, infer from share count in metadata. 
        If they specified a weight then infer the amount of shares
        """

        has_qty : bool      = init_quantity is not None
        has_weight : bool   = init_weight is not None

        if has_qty == has_weight:
            raise ValueError("Either specify quantity OR starting weight. Must have exactly one")
        
        price0 = self.market.price().iloc[0]
        tickers = price0.index.values

        valid_at_start = price0.dropna().index

        if has_weight: #get qty
            if isinstance(init_weight, str):
                if init_weight == 'uniform':
                    n = len(tickers) + 1 #cash
                    init_weight = pd.Series(0.0, index=tickers)
                    init_weight[valid_at_start] = 1/n
            
            init_weight = init_weight.reindex(tickers).fillna(0)
            if init_weight.sum() <= 0:
                raise ValueError("Weights must sum to a positive value!")
            weight = init_weight / init_weight.sum()
            quantity = (self.mv0 * init_weight)  / price0
            
            return weight, quantity.fillna(0)

        else: #get weight
            quantity : pd.Series = init_quantity.reindex(tickers).fillna(0)
            self.mv0 = (quantity * price0).sum()
            if self.mv0 <= 0:
                raise ValueError("Market Value can not be zero!")
            weight : pd.Series = (quantity * price0) / self.mv0
            
            return weight, quantity

    def get_returns(self, freq : str = None, by_constituent = False) -> pd.Series | pd.DataFrame:
        """
        Returns the returns of a portfolio with non-empty weight df
        freq : str, optional
            Pandas offset alias (e.g., 'D', 'W', 'H'). If provided, 
            returns are resampled to this frequency.
        by_constituent : bool , optional
            Will return a dataframe instead
        """
        if self.quantity is None:
            raise ValueError("Portfolio has not been backtested yet.")

        prices = self.market.price(field="close")

        mv = (self.quantity * prices)
        
        if not by_constituent:
            mv = mv.sum(axis=1)

        returns = mv.pct_change().fillna(0)

        if freq:
            returns = returns.resample(freq).apply(lambda x: (1 + x).prod() - 1).dropna()
        
        return returns
    
    def clear_cache(self):
        """
        Helper to clear cached data if portfolio data changes
        """
        self._returns = None


