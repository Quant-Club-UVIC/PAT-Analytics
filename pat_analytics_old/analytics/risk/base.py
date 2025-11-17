import pandas as pd
import numpy as np

from pat_analytics.analytics.base import AnalyticsBase, GroupMixin

class RiskBase(AnalyticsBase, GroupMixin):

    def __init__(self, portfolio, metadata):
        super().__init__(portfolio, metadata)
        self.anualized = True
    
    @property
    def var(self):
        #lazy importing
        from pat_analytics.analytics.risk import VaRAnalytics
        return VaRAnalytics(self.portfolio)


    