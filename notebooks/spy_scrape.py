"""
A script to read the list of constituents of spy from 
wikapedia
"""
import pandas as pd
import requests
from pathlib import Path

cwd =  Path.cwd().resolve()
data_dir = cwd / 'data'
fname = 'spy_constituents.csv'

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# have to add this to look more like a real browser
headers = {"User-Agent": "Mozilla/5.0"}
html = requests.get(url, headers=headers).text


sp500 = pd.read_html(html, header=0)[0]

sp500.to_csv(data_dir / fname)

print(f"Updated {data_dir / fname}")