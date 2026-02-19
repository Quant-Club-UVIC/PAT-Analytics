from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

from pat_analytics import Market, Portfolio
from pat_analytics.strategy import BuyNHold, StratConfig
from pat_analytics.backtesters import Backtester
from pat_analytics.metrics import RiskReport, PerformanceReport


data_dir = Path.cwd().parent / "sample-data"
tickers = ["AAPL", "SPY", "LULU"]

csv_paths = [data_dir / f"{s}.csv" for s in tickers]

market = Market.from_csv(filepaths = csv_paths, date_col= 'epoch', unit='s')

port = Portfolio(market, init_weight='uniform')
config = StratConfig()
strat = BuyNHold(config=config)
bt = Backtester(port, market, strat)

bt.run()
rr = RiskReport(bt.portfolio, market, resample_freq='D')
rr

pr = PerformanceReport(bt.portfolio, market)
pr.plot_returns().show()