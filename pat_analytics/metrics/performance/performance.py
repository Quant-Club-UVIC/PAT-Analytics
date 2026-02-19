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
        Dynamically applies rangebreaks based on data frequency.
        """
        returns = self.portfolio.get_returns()
        
        # Ensure correct DatetimeIndex
        plot_index = pd.to_datetime(returns.index, unit='s' if returns.index.dtype == 'int64' else None)
        cum_ret = (1 + returns).cumprod() - 1

        # DYNAMIC FREQUENCY CHECK
        # Calculate the median time difference between points
        if len(plot_index) > 1:
            time_delta = pd.Series(plot_index).diff().median()
            is_intraday = time_delta < pd.Timedelta(days=1)
        else:
            is_intraday = False

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=plot_index,
            y=cum_ret.values,
            mode="lines",
            name="Portfolio Strategy",
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>Date</b>: %{x}<br><b>Return</b>: %{y:.2%}<extra></extra>'
        ))

        fig.update_layout(
            title={'text': "Portfolio Cumulative Returns", 'x': 0.5},
            xaxis_title="Date",
            yaxis_title="Cumulative Returns (%)",
            yaxis_tickformat='.2%',
            template="plotly_white",
            hovermode="x unified"
        )

        # APPLY RANGEBREAKS CONDITIONALLY
        r_breaks = [dict(bounds=["sat", "mon"])] # Always hide weekends
        
        if is_intraday:
            # Only hide non-trading hours if we are on intraday frequency
            r_breaks.append(dict(bounds=[16, 9.5], pattern="hour"))
            print("Intraday detected: Hiding overnight hours.")
        else:
            print("Daily+ frequency detected: Showing full days.")

        fig.update_xaxes(rangebreaks=r_breaks)

        return fig

    def total_return(self):
        """A simple scalar metric for the report"""
        returns = self.portfolio.get_returns()
        return (1 + returns).cumprod().iloc[-1] - 1