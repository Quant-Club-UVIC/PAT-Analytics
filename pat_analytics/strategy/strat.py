"""
strat.py
"""

import pandas as pd
import numpy as np

from pat_analytics import Portfolio, Market

class StratConfig:
    """
    Configuration for strategy,
    sets up the environment the strategy 
    is done in
    """

    def __init__(self, 
                 rebalance="None",
                 commission_type="proportional",
                 commission_fee=0.00):
        """
        Configuration for the strategy
        """
        self.rebalance = rebalance
        self.commission_fee = commission_fee
        self.commission_type = commission_type

        
class Strategy:
    """
    Base class for strategy
    """
    def __init__(self, 
                 config : StratConfig = StratConfig()):
        
        self.config = config


    def initialize(self):
        pass



