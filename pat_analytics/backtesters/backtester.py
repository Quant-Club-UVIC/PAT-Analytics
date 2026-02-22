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
        Runs portfolio through market, allowing CASH to go negative
        to track total spend and transaction costs.
        """

        gamma = self.strategy.config.commission_rate
        f0 = self.strategy.config.commission_fee

        index = self.market.price_data.index
        tickers = self.market.price_data.columns.levels[0]

        stock_tickers = [t for t in tickers if t != 'CASH']

        q_prev = self.portfolio.q0.reindex(tickers).fillna(0.0)
        q_df = pd.DataFrame(index=index, columns=tickers, dtype=float)
        q_df.iloc[0] = q_prev

        for i in range(1, len(index)):
            t_cur = index[i]
            px_cur = self.market.price_data.loc[t_cur].xs("close", level=1).reindex(tickers)
            
            
            w_target = self.strategy.decide(portfolio=self.portfolio.up_to(t_cur), 
                                        market=self.market.up_to(t_cur))

            if w_target is not None:
                w_s = w_target.reindex(stock_tickers).fillna(0.0)
                p_s = px_cur[stock_tickers]
                q_s = q_prev[stock_tickers]
                
                dq_s = find_quantity(w_s, p_s, q_s, q_prev['CASH'], fee_rate=gamma, f0=f0)
                
                q_new = q_prev.copy()
                q_new[stock_tickers] += dq_s

                trade_outflow = (dq_s * p_s).sum()
                fees = (dq_s * p_s).abs().sum() * gamma + (dq_s != 0).sum() * f0
                q_new['CASH'] = q_prev['CASH'] - trade_outflow - fees
            else:
                q_new = q_prev

            q_df.loc[t_cur] = q_new
            q_prev = q_new
        
        #compute weight df at the end 
        prices = self.market.price(field="close").reindex(columns=q_df.columns)

        if 'CASH' in prices.columns:
            prices['CASH'] = 1.0

        mv_df = q_df * prices

        total_mv_per_day = mv_df.sum(axis=1)

        w_df = mv_df.divide(total_mv_per_day, axis=0).fillna(0.0)

        self.portfolio.quantity = q_df
        self.portfolio.weight = w_df