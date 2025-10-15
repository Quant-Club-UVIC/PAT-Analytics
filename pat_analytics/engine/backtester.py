import pandas as pd

class BaseBacktester:
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.prices : pd.DataFrame = portfolio.close
        self.returns : pd.DataFrame = portfolio.returns 
        self.q0 : pd.DataFrame = portfolio.q0
        self.w0 : pd.DataFrame = portfolio.w0
    
    def run(self):
        raise NotImplementedError
