import pandas as pd
import numpy as np

class AnalyticsBase:
    def __init__(self, portfolio):
        self.portfolio = portfolio

        #lazy cache
        self._returns = None
        self._weights = None
        self._market_value = None

    @property
    def returns(self) -> pd.Series:
        """
        Portfolio Total Returns
        """
        if self._returns is None:
            self._returns = self.portfolio.get_total_returns()
        return self._returns
    
    @property
    def weights(self) -> pd.DataFrame:
        """
        Portfolios Asset Weights
        """
        if self._weights is None:
            self._weights = self.portfolio.weight
        return self._weights
    
    @property
    def market_value(self) -> pd.Series:
        """
        Market Value in $
        """
        if self._market_value is None:
            self._market_value = self.portfolio.get_market_value()
        return self._market_value