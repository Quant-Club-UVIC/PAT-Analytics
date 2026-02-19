from pat_analytics.data import AlphaVantageLoader
import config # where api_key is stored
import time
from pathlib import Path

loader = AlphaVantageLoader(config.api_key)

output_dir = Path("./sample-data")
output_dir.mkdir(exist_ok=True)

tickers = ["SBUX", "EL", "DNUT", "YUM", "AAPL"]

for ticker in tickers:
    print(f"Fetching daily data for {ticker}...")

    #fetching the last 100 days
    df_daily = loader.get_daily_px(ticker, output_size='compact')
    
    csv_path = output_dir / f"{ticker}.csv" 
    
    df_daily.to_csv(csv_path)
    time.sleep(15) 

# download ETF Metadata (Example for SPY)
ticker_etf = 'SPY'
print(f"\nFetching metadata for {ticker_etf}...")
metadata = loader.get_etf_profile(ticker_etf)

# Extracting data from the returned dictionary
df_constit = metadata['holdings']
df_constit.to_csv(output_dir / f'{ticker_etf}_constit.csv', index=False)

print(f"{ticker_etf} Profile:")
print(f"- Inception: {metadata['inception']}")
print(f"- Div Yield: {metadata['div_yield']}")
print(f"- Expense Ratio: {metadata['expense_ratio']}")