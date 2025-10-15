import pandas as pd
import numpy as np

from pat_analytics.analytics.base import AnalyticsBase

class RiskBase(AnalyticsBase):

    def __init__(self, portfolio, window = 252):
        super().__init__(portfolio)