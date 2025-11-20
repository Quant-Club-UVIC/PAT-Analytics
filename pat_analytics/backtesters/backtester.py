"""
backtester.py
Defines the backtester class
"""
import pandas as pd
import numpy as np

from pat_analytics import Market, Portfolio
from pat_analytics.strategy import Strategy
from pat_analytics.utils.trade import update_weights, find_quantity

class Backtester:
    """
    Evolves the weights of a portfolio thru time, given 
    trading decisions made by a model, using data from
    Market
    """
    def __init__(self, 
                 portfolio : Portfolio, 
                 market : Market, 
                 strategy: Strategy):
        """
        Constructor for Backtester
        """
        self.portfolio = portfolio
        self.market = market
        self.strategy = strategy

    def run(self):
        """
        Runs the portfolio thru the market
        """
        index = self.market.price_data.index
        tickers = self.market.price_data.columns

        w0 : pd.Series = self.portfolio.w0
        q0 : pd.Series = self.portfolio.q0

        w_df = pd.DataFrame(columns=tickers, index=index, dtype=float)
        q_df = pd.DataFrame(columns=tickers, index=index, dtype = float)

        w_df.iloc[0] = w0
        q_df.iloc[0] = q0

        w_prev = w0
        q_prev = q0

        def close_at(t):
            return self.market.price_data.loc[t].xs("close", level=1)
        

        for i in range(1, len(index)):
            t_prev = index[i - 1]
            t_cur = index[i]
            
            self.portfolio.weight = w_df.loc[:t_prev].copy()
            self.portfolio.quantity = q_df.loc[:t_prev].copy()

            p_t : Portfolio = self.portfolio.up_to(t_cur)
            m_t : Market = self.market.up_to(t_cur)

            #make a decision
            w_target = self.strategy.decide(portfolio = p_t,
                                        market = m_t)

            close_cur = close_at(t_cur)
            close_prev = close_at(t_prev)

            if w_target is None: #no decision was made, just let it drift
                q_new = q_prev
            
            else: #TODO include fees
                w_target = w_target.reindex(tickers).fillna(0.0) #reindex
                w_target /= w_target.sum()

                q_new = find_quantity(w_target, close_prev, close_cur)
            
            mv_new = (q_new * close_cur).sum()
            w_new = (q_new * close_cur) / mv_new

            #store
            w_df.loc[t_cur] = w_new
            q_df.loc[t_cur] = q_new

            #update
            w_prev = w_new
            q_prev = q_new
            
        
        self.portfolio.weight = w_df
        self.portfolio.quantity = q_df