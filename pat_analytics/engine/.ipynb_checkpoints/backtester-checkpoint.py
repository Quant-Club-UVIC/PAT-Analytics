import pandas as pd

class BaseBacktester:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.prices : pd.DataFrame = portfolio.close
        self.net_returns : pd.DataFrame = 1 + portfolio.returns 
        self.q0 : pd.DataFrame = portfolio.q0
        self.w0 : pd.DataFrame = portfolio.w0
        self.rebalance_period : pd.Timedelta = portfolio.rebalance_period
    
    def run(self):
        raise NotImplementedError
