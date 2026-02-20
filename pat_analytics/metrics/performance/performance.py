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

    def plot_returns(self, by_constituent=False):
        """
        Generates and displays the Plotly chart for cumulative returns.
        Supports both total portfolio and individual constituent plotting.
        """
        returns = self.portfolio.get_returns(by_constituent=by_constituent)
        
        plot_index = pd.to_datetime(returns.index, unit='s' if returns.index.dtype == 'int64' else None)
        
        cum_ret = (1 + returns).cumprod() - 1

        # DYNAMIC FREQUENCY CHECK
        if len(plot_index) > 1:
            time_delta = pd.Series(plot_index).diff().median()
            is_intraday = time_delta < pd.Timedelta(days=1)
        else:
            is_intraday = False

        fig = go.Figure()

        if by_constituent:
            # Loop through each column (ticker/asset) and add a line
            for column in cum_ret.columns:
                fig.add_trace(go.Scatter(
                    x=plot_index,
                    y=cum_ret[column],
                    mode="lines",
                    name=str(column),
                    hovertemplate=f'<b>{column}</b><br>Date: %{{x}}<br>Return: %{{y:.2%}}<extra></extra>'
                ))
        else:
            # Standard portfolio view
            fig.add_trace(go.Scatter(
                x=plot_index,
                y=cum_ret.values,
                mode="lines",
                name="Portfolio Strategy",
                line=dict(color='#1f77b4', width=2),
                hovertemplate='<b>Portfolio</b><br>Date: %{x}<br>Return: %{y:.2%}<extra></extra>'
            ))

        fig.update_layout(
            title={'text': "Cumulative Returns" + (" by Constituent" if by_constituent else ""), 'x': 0.5},
            xaxis_title="Date",
            yaxis_title="Cumulative Returns (%)",
            yaxis_tickformat='.2%',
            template="plotly_white",
            hovermode="x unified" if not by_constituent else "closest"
        )

        # APPLY RANGEBREAKS
        r_breaks = [dict(bounds=["sat", "mon"])]
        if is_intraday:
            r_breaks.append(dict(bounds=[16, 9.5], pattern="hour"))
        
        fig.update_xaxes(rangebreaks=r_breaks)

        return fig
    
    def total_return(self):
        """A simple scalar metric for the report"""
        returns = self.portfolio.get_returns()
        return (1 + returns).cumprod().iloc[-1] - 1