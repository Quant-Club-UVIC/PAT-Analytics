from MarketData import MarketData
import config

import pandas as pd
import datetime

date_start = datetime.date(2021, 8, 1)
date_end = datetime.date(2021, 10, 1)
data = MarketData(config.api_key, (date_start, date_end))
df = data.getPxAction('AAPL', month='2023-08')
df.to_csv('AAPL.csv')