import pandas as pd
import numpy as np
from .backtester import BaseBacktester
import time

class ProportionalBacktester(BaseBacktester):
    """
    Evolve the portfolio with no rebalance
    """
    def __init__(self, portfolio, fee : float = 0.0, cash : float = 0.0):
        super().__init__(portfolio)
        self.rebalance_period = portfolio.rebalance_period
        self.fees = fee
        self.cash = cash
        
    def run(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run the backtest : evolve the portfolio weights with proportional rebalancing
        """
        weights = pd.DataFrame(columns=self.net_returns.columns, index=self.net_returns.index, dtype=float)
        weights.iloc[0] = self.w0

        q_df = pd.DataFrame(columns=self.net_returns.columns, index=self.net_returns.index, dtype = float)
        q_df.iloc[0] = self.q0 

        time_last_rebalance = self.net_returns.index[0]

        
        
        #evolve in time
        for idx, t in enumerate(self.net_returns.index[:-1], start=1):

            prev_R = self.net_returns.iloc[idx - 1]
            prev_q = q_df.iloc[idx - 1]

            if t - time_last_rebalance > self.rebalance_period: #rebalance
                time_last_rebalance = t
                weights.iloc[idx] = self.w0
        
                
                prev_px = self.prices.iloc[idx]
                V_pre = prev_px * prev_q + self.cash
                delta_q = self.proportional_fee_solver( prev_px, self.w0, prev_q, self.cash, self.fees)
                q_new = prev_q + delta_q
                q_df.iloc[idx] = q_new
                
                V_final = q_new * prev_px
                V_ftotal = V_final.sum()
                a = prev_px * delta_q
                a = a.abs()
                fee_tot = self.fees * a.sum() # rebalence fee total
                cash = V_pre - V_ftotal - fee_tot

            else: # no rebalance
                prev_w = weights.iloc[idx - 1]
                market_growth = prev_w @ prev_R
                weights.iloc[idx] = (prev_w * prev_R) / market_growth
                q_df.iloc[idx] = prev_q

        return weights, q_df, self.cash



    def proportional_fee_solver(self, p_cur : pd.Series, 
                                w0 : pd.Series,  
                                q_cur  : pd.Series, 
                                cash : float, 
                                fee_rate : float) ->  pd.Series:

        """
        Given the desired weights w0, fee rate, current price,
        and new cash, compute how to adjust quantity of shares to reach 
        desired weight w0 when there is a fee for every trade
        """
        ind = p_cur.index.to_list()
        # C cash added to account
        # fee_rate is the trade fee rate
    
        p = p_cur.to_numpy() # new stock price
        w0 = w0.to_numpy()  #  the desired weights
        q = q_cur.to_numpy() # the quantity of each share
    

        V_pre = np.sum(p * q) # V_pre is the total portfolio value without cash added, q * p
        p, w0, q = map(np.asarray, (p, w0, q))

        s = np.sign(w0 * (V_pre + cash) / p - q)  # guess trade direction

    
        # vector interstep for elementwise multiplication
        a = w0 / p
        b = (w0 * (V_pre + cash)) / p - q
    
        # signed traded value scalar
        S = (p @ (s * b)) / (1 + fee_rate * (p @ (s * a)))
    
        # final delta q solution
        delta_q = b - fee_rate * a * S

        return pd.Series(delta_q, index=ind)