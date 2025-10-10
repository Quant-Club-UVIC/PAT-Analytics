import pandas as pd
from typing import Dict


class Portfolio:

    def __init__(self, name, currency, positions):
        self.name = name
        self.currency = currency
        self.positions = Dict[str:float] # [ticker: amount held in $]

    def add_positons(self, value, ticker):
        self.positions[ticker] = self.positions.get(ticker, 0.0) + value
    
    def delete_position(self, ticker):
        """Removes postion from portfolio"""
        if ticker in self.positions:
            del self.positions[ticker]

    def portfolio_val(self):
        """calculates the sum of the amount held in each position to calculate full portfolio value"""
        return sum(self.positions.values())
    
    def weights(self):
        """create a dictionary for tickers and their weighting in the portfolio"""
        total = self.portfolio_val()
        weights = {ticker: value / total for ticker, value in self.positions.items()}
        
        return weights

