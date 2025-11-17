"""
strat.py
"""

import pandas as pd
import numpy as np

class StratConfig:
    """
    
    """

    def __init__(self, 
                 rebalance="None",
                 commission_type="proportional",
                 commission_fee=0.00):
        """
        Configuration for the 
        """
        self.rebalance = rebalance
        self.commission_type = commission_fee
        self.commission_type = commission_type

        
class Strategy:
    """
    Base class for strategy
    """
    def __init__(self):
        pass

    def initialize(self):
        pass



