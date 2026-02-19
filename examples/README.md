# Examples

We will show case examples!

## Getting the Data

We will be using alpha-vantage to get our data for now. Head over to [alphavantage.com](https://www.alphavantage.co/), click on get a free api key.  
Make a config.py file in examples/ in the form 
```python3
api_key = "secret_api_key123"
```
Open scrapeMarketData.py and adjust to the tickers you are interested in, then run
```bash
python3 scrapeMarketData.py
```
We are downloading the previous 100 days of daily price. Also gets some facts about SPY for example. This might take a bit  

## Running the Backtester + VaR + Chart
Go to QuickStarting.ipynb, fill in your tickers and run!

## More Complicated Strategies
Soon...