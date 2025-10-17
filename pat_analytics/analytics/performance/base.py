import pandas as pd
import numpy as np

from pat_analytics.analytics.base import AnalyticsBase

class PerformanceBase(AnalyticsBase):
    
    def __init__(self, portfolio):
        super().__init__(portfolio)