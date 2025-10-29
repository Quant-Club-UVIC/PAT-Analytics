import pandas as pd
import numpy as np
from pat_analytics.analytics.base import AnalyticsBase
class PerformanceRatios(AnalyticsBase):
    def _init_(self, portfolio):
        super()._init_(portfolio)
    
    def calculate_Beta(self, benchmark_returns: pd.Series)->float:

        variance=np.var(benchmark_returns)
        covariance=np.cov(self.returns, benchmark_returns)[0][1]
        beta= covariance/variance

        return beta
    def calculate_Sharpe(self, risk_free_rate: float)->float:
        #risk_free rate=bond usually 3%-5%
        excess_returns=self.returns - risk_free_rate
        risk=np.std(self.returns)
        sharpe_ratio=np.mean(excess_returns)/risk

        return sharpe_ratio
    def calculate_Treynor(self, risk_free_rate: float, benchmark_returns: pd.Series)->float:
        excess_returns=self.returns - risk_free_rate
        beta=self.calculate_Beta(benchmark_returns)
        treynor_ratio=np.mean(excess_returns)/beta

        return treynor_ratio

    def calculate_alpha(self, risk_free_rate: float, benchmark_returns: pd.Series) -> float:
        
        beta = self.calculate_Beta(benchmark_returns)
        expected_return = risk_free_rate + beta * (np.mean(benchmark_returns) - risk_free_rate)
        alpha = np.mean(self.returns) - expected_return

        return alpha
    def calculacate_sortino(self, risk_free_rate: float)->float:
        excess_returns=self.returns - risk_free_rate
        negative_returns=excess_returns[excess_returns<0]
        downside_deviation=np.std(negative_returns)
        sortino_ratio=np.mean(excess_returns)/downside_deviation

        return sortino_ratio


