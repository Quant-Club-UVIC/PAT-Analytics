"""
risk.py

"""
from pat_analytics.metrics.report import Report
import pandas as pd
import numpy as np
import json

class RiskReport(Report):
    def __init__(self, portfolio, market, window=252, level = 0.95, resample_freq = None):
        """
        portfolio      : Portfolio object with quantity data
        market         : Market object
        window         : Observation window
        level          : Confidence level (0.95 = 95%)
        resample_freq  : Pandas offset alias (e.g., 'D' for daily, 'W' for weekly, 'H' for hourly)
                         If None, uses the raw frequency of the backtest.                  
        """
        self.portfolio = portfolio
        self.market = market
        self.window = window
        self.level = level
        self.resample_freq = resample_freq

        #Cache for lazy loading
        self._var = None
        self._cvar = None


    @property
    def var(self):
        """
        Implementation of vanilla
        Historic Value at Risk
        """
        if self._var is None:
            losses = - self.portfolio.get_returns(freq = self.resample_freq)
            self._var = losses.quantile(self.level)
        
        return self._var
    
    @property
    def cvar(self):
        """
        Implementaton of 
        Conditional Value at Risk
        """

        if self._cvar is None:
            losses = - self.portfolio.get_returns(freq = self.resample_freq)
            current_var = self.var

            tail_losses = losses[losses >= current_var]
            self._cvar = tail_losses.mean()

        return self._cvar
    
    def to_dict(self):
        """
        Returns a dictionary of all calculated risk 
        metrics.
        """
        freq = pd.infer_freq(self.portfolio.get_returns().index)
        return {
            "time_scale" : freq or "custom",
            "confidence_level" : self.level,
            "window" : self.window,
            "var" : self.var,
            "cvar" : self.cvar
        }
    
    def __repr__(self):
        """
        Defines the default output when printing obj
        """
        return f"RiskReport({json.dumps(self.to_dict(), indent=4)})"
    
    def __str__(self):
        return str(self.to_dict())
    