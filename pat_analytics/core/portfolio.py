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
            new_port.quantity = self.quantity.loc[time].copy()
        
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

        if has_weight: #get qty
            if isinstance(init_weight, str):
                if init_weight == 'uniform':
                    n = len(tickers) + 1 #cash
                    init_weight = pd.Series( 1 / n, index=tickers, name = 'weight')
            
            init_weight = init_weight.reindex(tickers).fillna(0)
            if init_weight.sum() <= 0:
                raise ValueError("Weights must sum to a positive value!")
            weight = init_weight / init_weight.sum()
            quantity : pd.Series = (self.mv0 * init_weight)  / price0
            
            return weight, quantity 

        else: #get weight
            quantity : pd.Series = init_quantity.reindex(tickers).fillna(0)
            self.mv0 = (quantity * price0).sum()
            if self.mv0 <= 0:
                raise ValueError("Market Value can not be zero!")
            weight : pd.Series = (quantity * price0) / self.mv0
            
            return weight, quantity




