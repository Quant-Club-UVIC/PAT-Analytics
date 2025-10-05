import requests
import datetime
import pandas as pd
import re

class MarketData():
    """
    Utility class for collecting market information
    """
    def __init__(self, api_key : str, date_range : tuple[datetime.date, datetime.date]):
        
        self.base_url = "https://www.alphavantage.co/query?"
        
        self.api_key = api_key
        self.date_start, self.date_end = date_range
    
    def datetimeDecompose(self, df : pd.DataFrame, dateCol : str, doEpoch : bool = True, doYear: bool = True,
                          doMonth : bool = True, doDay : bool = True, doHour : bool = True,
                          doMinute : bool=True, doSecond : bool=False, inplace : bool=True) -> pd.DataFrame | None:
        """
        Pass a dataframe with a datetime column,
        decompose it into year, month, day, hour, minute.
        The do flags specify how finely you want it decomposed.
        Defaulted to inplace    
        """
        if not inplace:
            df = df.copy()

        if dateCol not in df:
            raise ValueError("The passed column does not exist in the df, try again")

        df[dateCol] = pd.to_datetime(df[dateCol], errors='raise')
   
        options = [
            (doYear, 'year', df[dateCol].dt.year),
            (doMonth,'month', df[dateCol].dt.month),
            (doDay, 'day', df[dateCol].dt.day),
            (doHour, 'hour', df[dateCol].dt.hour),
            (doMinute, 'minute', df[dateCol].dt.minute),
            (doSecond, 'second', df[dateCol].dt.second),
            (doEpoch, 'epoch', df[dateCol].astype('int64') // 10**9)
        ]
        
        for flag, col, value in options:
            if flag:
                df[col] = value

        if not inplace:
            return df

        return None
    
    def getPxAction(self, ticker : str, interval : str = '5min', extended_hours : bool = False,
                    month : str | None = None, output_size : str = 'full') -> pd.DataFrame:
        """
        Call the api to get a certain ticker as a df,
        with index as epoch timestamps, ohlc, and 
        year, month, day, hour, minute of the price
        ----
        Usage:
        >>> getPxAction('IBM', 'demo').head(1)
        epoch       |year   |month  |day    |hour   |minute |open   |high   |low    |close  |
        =====================================================================================
        1759521300  |2025   |10     |03     |19     |55     |288.39 |288.75 |288.39 |288.45 |
        """
        #sanitize the input (so that we dont use up an api on erroneous calls)
        allowed_intervals = ['1min', '5min', '15min', '30min', '60min']
        assert (interval in allowed_intervals), "ERROR: Invalid interval entered."

        if month:
            assert re.fullmatch(r"(20[0-2]\d{1})-(0[1-9]|1[0-2])", month), "ERROR: Invalid year-month entered"

        
        #the api call
        url = (
            self.base_url + 
            "function=TIME_SERIES_INTRADAY&" 
            f"symbol={ticker}&" 
            f"interval={interval}&" 
            f"apikey={self.api_key}&" 
            f"datatype=csv&"
            f"extended_hours={'true' if extended_hours else 'false'}&"
            f"outputsize={output_size}&"
            f"{('month='+month) if month else ''}"

        )

        df = pd.read_csv(url)
        
        self.datetimeDecompose(df, 'timestamp')
        
        df = (df
            .set_index('epoch')
            .reindex(columns=[ 'year', 'month', 'day', 'hour', 'minute', 
                        'open', 'high', 'low', 'close', 'volume']))

        return df

    def getETFmetadata(self, ticker : str) -> tuple[pd.DataFrame, float, str, float]:
        """
        Returns and etfs constituents as a df,
        div_yield, inc_date. Dfs columns are ['ticker', 'name', 'weight']
        """
        url = (
            self.base_url + 
            'function=ETF_PROFILE&'
            f'symbol={ticker}&'
            f'apikey={self.api_key}'
        )
        data = requests.get(url).json()
        
        div_yield = float(data['dividend_yield'])
        inc_date = data['inception_date']
        net_expense_ratio = float(data['net_expense_ratio']) #comission fee
        data = data['holdings']

        df = pd.json_normalize(data)
        df = df.rename(columns={'symbol' : 'ticker',
           'description' : 'name'})
        df['weight'] = df['weight'].astype('float')

        return df, div_yield, inc_date, net_expense_ratio

                