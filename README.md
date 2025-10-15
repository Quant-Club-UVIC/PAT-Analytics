# PAT-Analytics
PAT-Analytics is a python library enabling user to fetch market data, create portfolios, display portfolio metrics : risk, sector allocations, implied growth, stress-tests. Allows access to models, and portfolio optimizers. 

# Quick Set-Up 
## For Users
If you wish to use the library, make sure to clone the repo and then 
```bash
pip3 install -e .
```  
Here is a simple script to get the VaR of a portfolio, with data
```python3
from pat_analytics import Portfolio, MarketData
tickers = ["LULU", "NVDA", "SPY"]
data = MarketData("my_secret_api_key").getPxActions(tickers)
p = Portfolio(data, weight='uniform')
print(p.risk.var)
```
Or if you do not want to call the API every time, here is an example of 
calculating sharpe by sector
```python3
from pat_analytics import Portfolios
tickers = {"LULU" : "lulu.csv", "NVDA" : "nvda.csv", "SPY" : "spy.csv"}
p = Portfolio.from_csv(tickers, weight='uniform')
print(p.performance.sharpe.by_sector())
```
## For Contributors
Need to install the necessary dependancies, after cloning the repo in main/ type  
```bash
python3.12 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```  

# Code-Base  
Main source-code is located in pat_analytics/ , the main object *Portfolio* is defined in portfolio.py. If you wish to see how to run our code check out examples/. All of our work-in-progress notebooks and scripts are in work-in-progress/.  

# To Contributors  
If you add dependencies to this project (pandas, requests, etc) you must update the requirements.txt, you can do this by  
```python3
pip3 install pipreqs  
pipreqs --force ./
```
Do this in main/ of course.  
If you have come up with a new model, add your whitepaper for it in documentation/, after review it will be added to the main .tex file
# Contributors  
Add here later