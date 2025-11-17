"""
performance.py
"""
import numpy as np
import pandas as pd

from pat_analytics.metrics.report import Report

class PerformanceReport(Report):
    def __init__(self):
        super().__init__()
