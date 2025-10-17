import pandas as pd
import numpy as np
from .backtester import BaseBacktester
import time

class SimpleBacktester(BaseBacktester):
    """
    Evolve the portfolio with no rebalance
    """
    def __init__(self, portfolio, fee : float = 0.0):
        super().__init__(portfolio)
        self.rebalance_period = portfolio.rebalance_period
        self.fees = fee

    def run(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run the backtest : evolve the portfolio weights with basic rebalancing
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

                added_cash = 0
                prev_px = self.prices.iloc[idx]
                q_new = self.rebalance(self.w0, prev_q, prev_px, added_cash)
                q_df.iloc[idx] = q_new

            else: # no rebalance
                prev_w = weights.iloc[idx - 1]
                market_growth = prev_w @ prev_R
                weights.iloc[idx] = (prev_w * prev_R) / market_growth
                q_df.iloc[idx] = prev_q

        return weights, q_df

    def rebalance(self, w0 : pd.Series, 
                  q_cur: pd.Series,
                  p_cur : pd.Series, 
                  cash: float) -> pd.Series:
        """
        Given the last weights, cost of trading, and current price,
        and new cash, compute how to adjust quantity of shares to reach 
        desired weight w0
        """
        mv_pre = (q_cur @ p_cur).sum()
        n = (q_cur != 0).sum() #how many non zero quantity tickers
        q_new = w0*(mv_pre + cash - n * self.fees) / p_cur
        #print(f"q_cur : \n{q_cur}\n r_cur : \n{r_cur}")
        #print(f"V pre mv{mv_pre}\nn ={n}\nq_new = {q_new}")
        return q_new