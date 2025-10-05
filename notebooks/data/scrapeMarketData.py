from MarketData import MarketData
import config

import pandas as pd
import datetime

date_start = datetime.date(2021, 8, 1)
date_end = datetime.date(2021, 10, 1)
data = MarketData(config.api_key, (date_start, date_end))
ticker = 'SPY'
df = data.getPxAction(ticker)
df.to_csv(f'{ticker}.csv')

ticker_etf = 'SPY'
df, div_yield, inc_date, ner = data.getETFmetadata(ticker_etf)
df.to_csv(f'{ticker_etf}_constit.csv')
assert (isinstance(div_yield, float) and isinstance(ner, float))
print(f"{ticker_etf} was incorporated in {inc_date}, and has a div yield of {div_yield}, and costs {ner}")