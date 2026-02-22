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

def find_quantity(w0: pd.Series, 
                  p_cur: pd.Series,  
                  q_cur: pd.Series, 
                  cash: float = 0.0, 
                  fee_rate: float = 0.0,
                  f0: float = 0.0) -> pd.Series:
    """
    Computes delta_q while protecting against NaNs and DivByZero
    """
    p_cur = p_cur.dropna()
    valid_idx = p_cur.index
    
    p = p_cur.values
    w = w0.reindex(valid_idx).fillna(0.0).values
    q = q_cur.reindex(valid_idx).fillna(0.0).values

    # if price 0, we can't trade it, set price to Inf so weight/p = 0.
    p_safe = np.where(p <= 1e-8, np.nan, p)
    
    v_pre = np.nansum(p * q)

    n_trades = np.count_nonzero(w - (q * p / (v_pre + 1e-9))) # estimate trades
    v_eff = v_pre + cash - (n_trades * f0)
    
    if v_eff <= 0:
        return pd.Series(-q, index=valid_idx) #DONT TRADE 

    a = np.divide(w, p_safe, out=np.zeros_like(w), where=p_safe > 0)
    b = np.divide(w * v_eff, p_safe, out=np.zeros_like(w), where=p_safe > 0) - q #amt to trade
    
    s = np.sign(b) #trade direction
    
    dot_pb = np.dot(p, s * b)
    dot_pa = np.dot(p, s * a)
    
    S = dot_pb / (1 + fee_rate * dot_pa) if (1 + fee_rate * dot_pa) != 0 else 0
    
    delta_q = b - (fee_rate * a * S)
    
    return pd.Series(delta_q, index=valid_idx).reindex(p_cur.index).fillna(0.0)