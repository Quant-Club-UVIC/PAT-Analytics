import pandas as pd
import numpy as np
from .backtester import BaseBacktester

class SimpleBacktester(BaseBacktester):
    """
    Evolve the portfolio with no rebalance
    """
    def __init__(self, portfolio):
        super().__init__(portfolio)

    def run(self) -> dict[str, pd.DataFrame]:
        """
        Run the backtest : evolve the portfolio weights without rebalancing
        """

        weights = pd.DataFrame(columns=self.returns.columns, index=self.returns.index, dtype=float)
        weights.iloc[0] = self.w0

        #copy the quantity in each row, since we dont change
        q_df = pd.DataFrame(np.tile(self.q0.values, (len(self.returns), 1)),
                            columns=self.q0.columns, index= self.q0.index)
        
        #evolve in time
        for t in range(1, len(self.returns)):
            prev_w = weights.iloc[t - 1]
            prev_R = self.returns.iloc[t - 1]
            market_value = prev_w @ prev_R
            weights.iloc[t] = (prev_w * prev_R) / market_value

        return weights, q_df