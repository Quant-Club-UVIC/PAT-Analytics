import numpy as np
import pandas as pd
from .base import RiskBase

class VaRAnalytics(RiskBase):
    def __init__(self, portfolio, window=252, level = 0.95):
        super().__init__(portfolio, window)
        self.level = level

    