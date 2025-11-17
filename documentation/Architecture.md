# PAT - Architectural Document 
## DISCLAIMER  
***NONE OF THIS CODE IS YET FUNCTIONAL, THESE ARE USER STORIES TO PROVIDE THE DEVELOPERS WITH DIRECTION, AND API WRITERS TO KNOW WHAT TO EXPECT*** 
## Overview
I begin with user usage of the application. If one wants to see metrics on a buy and hold portfolio they will
```python3
from pat_analytics import MarketData, Market, Portfolio
from pat_analytics.models import Simple
from pat_analytics.metrics import RiskReport, PerformanceReport

tickers = ["SPY", "LULU", "NVDA", "DNUT", "CASH-CAD"]

#where the data will be stored
m = Market.from_alphavantage(
    api_key="my_secret_api_key",
    tickers=tickers,
    start="2000-01-01",
    end="2025-01-01")

#portfolio intializers
p = Portfolio(tickers=tickers, weight='uniform')

#how buy and sell decisions are made
model = Simple(
    rebalance = "1M",
    commision_type = "proportional",
    commision_fee="0.05"
)

bt = Backtester(
    market = m,
    model = model,
    portfolio = p,
)

result = bt.run()
risk = RiskReport(p, market)
perf = PerformanceReport(p, market)

print(f"Sharpe : {risk.sharpe()}")
print(f"Beta by sector : {risk.by_sector.beta()}")
```  
This examples shows the 5 main componenets of PAT:  
- Market  
- Portfolio  
- Backtester  
- Models
- Metrics  
We initialize a market with data on price, earnings reports, industry and sector, macro factors. These are dataframes containing all of this. Next we can create a portfolio with a starting weight (what positions it holds). In order to evolve this portfolio through time, we use the Backtester, which handles the effect of moving prices on our portfolio weights. To make this interactive, we can make a model. A model makes decisions of buy, hold or sell in the portfolio based on the existing market information. At any point you are able to access portfolio metrics.  

## Implementation  
This section will include implementation details on the four parts and exactly how they interact.

### Market
The Market object provides the user with fetching raw data, normalizing and retrival. Is also used by the other components of PAT-Analytics 

#### Internal Structure  
A Market object can be fully characterized using a set of timeseries, representing the available data on the market  
- price_data : pd.DataFrame  
  - index: datetime
  - columns: Multiindex[ticker, field], field is one of open, high, low, close, volume
  - contains the price of a position at a certain time
- dividend_data : pd.DataFrame
  - index: datetime
  - columns: ticker
  - contains the dividend of a position paid out and when
- fundemental_data : pd.DataFrame
  - index: datetime
  - columns: Multiindex[ticker, field], field is one of EPS, Earnings, Revenue ...
  - Contains fundemental data and for what quarter
- meta_data : pd.DataFrame  
  - index: tickers 
  - columns: {sector, industry, currency, exchange} 
- macro_data : pd.DataFrame
  - index: datetime
  - columns: treasury bills
  - Contains the rates of the treasury bills for now. Later will include other macro factors (CPI, Inflation etc)
- fx : pd.DataFrame 
  - index: Currency Name 
  - columns: Multiindex[ticker, field], field is one of open, high, low, close, volume 
  - Contains the exchange rate between USD and Currency Name
  
#### Data Loading  
Data loading can be done through a couple of ways, here are some valid ones:
```python3 
Market.from_alphavantage(api_key, tickers, start, end)
Market.from_csv(path)
```

#### Data Access
In order to access market data, we provide a couple of examples  
```python3
market = Market.from_alphavantage(...)
market.price("AAPL") #get a timeseries of AAPL stock
market.fundemental("TSLA", "EPS") #get latest EPS of Tesla
```
### Portfolio
The Portfolio object is a container of weights and quantity of stock one holds thru time, given a strategy. The main features of Portfolio are 
- weights : pd.DataFrame  
  - index: datetime
  - columns: tickers
  - Keeps track of the weight of each position
- quantity: pd.DataFrame 
  - index: datetime
  - columns: tickers
  - Keeps track of the quanity of shares of each position

#### Usage  
To interact with a Portfolio object you must specify a starting weight 
```python3
tickers = ["NVDA", "DNUT"]
weight = {
    'NVDA' : 0.1,
    'DNUT' : 0.9
}
p = Portfolio(market, weight=weight)
```

### Backtester

### Analytics

### Models