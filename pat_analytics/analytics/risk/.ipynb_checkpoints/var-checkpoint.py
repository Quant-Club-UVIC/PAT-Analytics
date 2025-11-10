import numpy as np
import pandas as pd
from .base import RiskBase

class VaRAnalytics(RiskBase):
    def __init__(self, portfolio, window=252, level = 0.95):
        super().__init__(portfolio)
        self.window = window
        self.level = level

    @property
    def var(self):
        """
        Implementation of vanilla
        Historic Value at Risk
        """
        net_returns : pd.Series = 1 - self.returns
        return net_returns.quantile(1 - self.level)
    
    @property
    def cvar(self):
        """
        Implementaton of 
        Conditional Value at Risk
        """

        net_returns : pd.Series = 1 - self.returns # calculate net returns

        threshold = np.percentile(net_returns, (1 - self.level) * 100) # This is var or the threshold

        tail_losses = net_returns[net_returns >= threshold] # create a variable for all of the losses beyond var

        return tail_losses.mean() # calculate cvar the mean of the potential losses
    
    