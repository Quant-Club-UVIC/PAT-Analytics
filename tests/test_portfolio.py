import unittest
from pat_analytics import Portfolio
import pandas as pd
import numpy as np

class testPortfolio(unittest.TestCase):

    def setUp(self):
        self.port = Portfolio()
        dates = pd.date_range(start = '2020-01-01', end = '2021-01-01', freq='5min')
        tickers = ["A", "B", "C", "D", "E"]
        
if __name__=="__main__":
    unittest.main()