# Notebooks ReadMe
Development notebooks 

## Quick Set Up  
Download and install the repo by 
```bash
git clone https://github.com/Quant-Club-UVIC/PAT.git
```
Set up your environment by 
```bash
conda env create -f environment.yml
conda activate PAT
```  
If you would like to use the MarketData class in data/ you will need to acquire an api key from [AlphaVantage](https://www.alphavantage.co/documentation/). Once you get it go into data/ and create python file named *config.py* in data/, this will hold your api keys. Make it of the form  
```python3
#config.py
api_key = "MY_SECRET_API_KEY"
```
You may check .gitignore, our config.py file will not be uploaded once you push. Must keep the keys secret from prying eyes. To get market data, run *scrapeMarketData.py*, specify the ticker and what functions you want. Check out the MarketData class.

