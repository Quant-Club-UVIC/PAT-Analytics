"""
backtester.py
Defines the backtester class
"""
import pandas as pd
import numpy as np

from pat_analytics import Market, Portfolio
from pat_analytics.models import Model

class Backtester:
    """
    Evolves the weights of a portfolio thru time, given 
    trading decisions made by a model, using data from
    Market
    """
    def __init__(self, portfolio : Portfolio, market : Market, model: Model):
        self.portfolio = portfolio
        self.market = market