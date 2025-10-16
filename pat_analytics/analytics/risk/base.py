import pandas as pd
import numpy as np

from pat_analytics.analytics.base import AnalyticsBase

class RiskBase(AnalyticsBase):

    def __init__(self, portfolio):
        super().__init__(portfolio)
        self.anualized = True
    
    @property
    def var(self):
        #lazy importing
        from pat_analytics.analytics.risk import VaRAnalytics
        return VaRAnalytics(self.portfolio)


    