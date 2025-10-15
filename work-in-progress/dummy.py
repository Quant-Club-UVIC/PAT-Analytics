import pandas as pd
import numpy as np

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

print(p.weight.head(10))
print(p.weight.tail(10))