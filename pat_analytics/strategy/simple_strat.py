"""
simple-strat.py
Implementation of the simple strategies
"""

import pandas as pd
import numpy as np

from .strat import Strategy
from pat_analytics import Portfolio, Market

class BuyNHold(Strategy):

    def decide(self,
               portfolio : Portfolio,
               market : Market) -> tuple[pd.Series]:
        """
        Decide
        """
        self.portfolio = portfolio
        self.market = market

        return None