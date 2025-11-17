from pathlib import Path
import pandas as pd

from pat_analytics import Market, Portfolio
from pat_analytics.metrics import RiskReport, PerformanceReport

parent_dir = Path.cwd().parent
data_dir = parent_dir / "sample-data"

tickers = ["AAPL", "SPY", "INTC"]
price_data = {}
for s in tickers:
    df = pd.read_csv(data_dir / f"{s}.csv")
    df['datetime'] = pd.to_datetime(df['epoch'], unit='s')
    df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
    price_data[s] = df

market = Market.from_dict(price_data)

print(market.tickers)
