"""
portfolio.py

Defines the Portfolio class
"""
import pandas as pd

class Portfolio:
    """
    
    """
    def __init__(self, init_weight = pd.Series | str, init_quantity = pd.Series | None):
        self.w0 = init_weight
        self.q0 = init_quantity
        
