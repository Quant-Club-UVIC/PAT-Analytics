"""
portfolio.py

Defines the Portfolio class
"""
import pandas as pd
from datetime import datetime

class Portfolio:
    """
    Portfolio class contains all information 
    regarding a portfolio
    """
    def __init__(self, init_weight : pd.Series | str = None, init_quantity : pd.Series = None, init_market_value : float = 1.0):
        """
        Canonical constructor of portfolio
        init_weight         : pd.Series [ticker] -> weight  | str (the weight of each position in the portfolio at the start)
        init_quantity       : pd.Series [ticker] -> quantity of stock (the quantity of each position in the portfolio at the start)
        init_market_value   : float (the starting market value of the portfolio in USD)
        User must provide either weight or quantity
        """
        self.w0 = init_weight
        self.q0 = init_quantity
        self.mv0 = init_market_value

        self.weight : pd.DataFrame = None
        self.quantity : pd.DataFrame = None

    
    def up_to(self, time : datetime):
        """
        Returns a copy of the portfolio
        but up to time t
        """
        new_port = Portfolio(self.w0, self.q0, self.mv0)

        if self.weight is not None:
            new_port.weight = self.weight.loc[:time].copy()
        
        if self.quantity is not None:
            new_port.quantity = self.quantity.loc[time].copy()
        
        return new_port