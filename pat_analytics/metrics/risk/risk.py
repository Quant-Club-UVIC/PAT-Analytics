"""
risk.py

"""
from pat_analytics.metrics.report import Report

class RiskReport(Report):
    def __init__(self, portfolio, market):
        self.portfolio = portfolio
        self.market = market

    