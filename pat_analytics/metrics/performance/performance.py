"""
performance.py
"""
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from pat_analytics.metrics.report import Report

class PerformanceReport(Report):
    def __init__(self, portfolio, market):
        self.portfolio = portfolio
        self.market = market

    def plot_returns(self):
        """
        Generates and displays the Plotly chart for cumulative returns.
        """
        returns = self.portfolio.get_returns()
        cum_ret = (1 + returns).cumprod() - 1

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=cum_ret.index,
            y=cum_ret.values,
            mode="lines",
            name="Portfolio Strategy",
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Date</b>: %{x}<br><b>Return</b>: %{y:.2%}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Portfolio Cum Returns Performance",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Date and Time",
            yaxis_title="Cumulative Returns (%)",
            template="plotly_white",
            hovermode="x unified"
        )

        # handle time gaps (Weekends and Outside Market Hours)
        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]),              # hide weekends
                dict(bounds=[16, 9.5], pattern="hour")   # hide 4pm - 9:30am
            ]
        )

        # 5. Format Y-axis as percentage
        fig.update_layout(yaxis_tickformat='.2%')

        return fig # Return the figure object so the user can call .show() or further modify it

    def total_return(self):
        """A simple scalar metric for the report"""
        returns = self.portfolio.get_returns()
        return (1 + returns).cumprod().iloc[-1] - 1