import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pat_analytics import Portfolio

import pandas as pd


stocks = ["LULU", "AAPL", "NVDA"]
data = {}
for s in stocks:
    df = pd.read_csv(f"{s}.csv")
    df['datetime'] = pd.to_datetime(df['epoch'], unit='s')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    data[s] = df


p = Portfolio.from_dict(data, weight = 'uniform')

p.run_backtest()

returns = p.get_total_returns().cumprod()
mv = p.get_market_value()

weight = p.weight.reset_index(drop=True)
print(weight)
weight.plot(title="Portfolio Weight Drift")
plt.show()

print(p.weight.tail(10))

print(f"The amount of shares : \n{p.quantity * p.close}")
print(f"The returns are {returns}")
print(f"The mv is {mv}")