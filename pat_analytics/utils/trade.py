"""
trade.py
A collection of utility functions
for computation related to trading
"""
import pandas as pd
import numpy as np


def update_weights(weight0 : pd.Series,
                   returns : pd.Series):
    """
    Given an initial weight, and returns,
    compute the new weight
    """
    return (weight0 * returns) / (weight0 @ returns)

def find_quantity(weight : pd.Series,
                  px_old : pd.Series,
                  px_new : pd.Series):
    """
    Given old price, new price, and a 
    target weight, compute the new quantity
    """