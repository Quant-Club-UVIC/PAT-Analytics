"""
report.py
"""

import numpy as np
import pandas as pd

class Report:
    """
    Parent class for all report classes
    """
    def __init__(self, portfolio, market):
        self.portfolio = portfolio
        self.market = market

    