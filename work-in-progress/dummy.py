import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pat_analytics import Portfolio

import pandas as pd


stocks = ["AAPL", "LULU", "NVDA", "SPY"]
weight = {}
data = {}
for s in stocks:
    df = pd.read_csv(f"{s}.csv")
    df['datetime'] = pd.to_datetime(df['epoch'], unit='s')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    data[s] = df


p = Portfolio.from_dict(data, weight = 'uniform', rebalance_period="5min")

p.run_backtest()

returns = p.get_total_returns().cumprod()
mv = p.get_market_value()

weight = p.weight.reset_index(drop=True)
print(weight)
weight.plot(title="Portfolio Weight Drift")
plt.show()

returns.reset_index(drop=True).plot(title="Portfolio Market Value")
plt.show()
print(p.weight.tail(10))

print(f"VAR {p.risk.var.var * 100 : .2f} %")