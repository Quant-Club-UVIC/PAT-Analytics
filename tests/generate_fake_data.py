import numpy as np
import pandas as pd

tickers = ["CompanyA", "CompanyB", "CompanyC", "CompanyD"]
T = 20000 # total amount of time steps
l = len(tickers)
px_action = np.random.rand(T,l)*0.1