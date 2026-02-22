from pat_analytics.data import AlphaVantageLoader
import config # where api_key is stored
import time
from pathlib import Path

loader = AlphaVantageLoader(config.api_key)

output_dir = Path("./sample-data")
output_dir.mkdir(exist_ok=True)

tickers = ["SBUX", "BABA", "CZR", "INTC", "META", "BRK.B", "LUMN", "SPY"]

for ticker in tickers:
    print(f"Fetching daily data for {ticker}...")

    #fetching the last 100 days
    df_daily = loader.get_daily_px(ticker, output_size='compact')
    
    csv_path = output_dir / f"{ticker}.csv" 
    
    df_daily.to_csv(csv_path)
    time.sleep(15) 
