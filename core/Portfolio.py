import pandas as pd


class Portfolio:

    def __init__(self, name, currency, positions):
        self.name = name
        self.currency = currency
        self.positions = {} # {ticker: amount held in $}

    def add_positons(self, value, ticker):
        self.positions[ticker] = value
        return self.positions
    
    def delete_position(self, ticker):
        if ticker in self.positions:
            del self.positions[ticker]

    def portfolio_val(self):
        value = 0
        for ticker in self.positions:
            value += self.postions[ticker]
        return value

    
    
    

