import requests
import datetime
import pandas as pd
import re
import io

class MarketData():
    """
    Utility class for collecting market information
    """
    def __init__(self, api_key : str, date_range : tuple[datetime.date, datetime.date]):
        
        self.base_url = "https://www.alphavantage.co/query?"
        
        self.api_key = api_key
        self.date_start, self.date_end = date_range

    def _safe_get(self, params : dict, mode : str, timeout: int = 10) -> io.StringIO | dict:
        """
        Validates api call before turning into tables, gives
        error msgs to api user from alphavantage
        """
        if mode not in ('json', 'csv'):
            raise ValueError("Error using _safe_get, must pass type as either csv or json")

        response = requests.get(self.base_url, params=params, timeout=timeout)

        if response.status_code != 200: #not ok
            raise ConnectionError(f"AlphaVantage returned HTTP {response.status_code} : {response.text}")

        return io.StringIO(response.text) if mode == 'csv' else response.json()
        
    
    """
    ============DATA=UTILITIES================
    """
    
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
    
    """
    ===========API=CALLS==================
    """    
    
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
        params = {
            "function" : "TIME_SERIES_INTRADAY", 
            "symbol" : ticker, 
            "interval" : interval, 
            "apikey" : self.api_key, 
            "datatype" : "csv",
            "outputsize" : output_size
        }
        if month:
            params['month'] = month

        params['extended_hours'] = 'true' if extended_hours else 'false'

        csv_stream = self._safe_get(params, mode = 'csv')
        df = pd.read_csv(csv_stream)
        
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
        params = {
            'function' : 'ETF_PROFILE',
            'symbol' : ticker,
            'apikey' : self.api_key
        }

        json_stream = self._safe_get(params, mode='json')

        data = (json_stream)
        
        div_yield = float(data['dividend_yield'])
        inc_date = data['inception_date']
        net_expense_ratio = float(data['net_expense_ratio']) #comission fee
        data = data['holdings']

        df = pd.json_normalize(data)
        df = df.rename(columns={'symbol' : 'ticker',
           'description' : 'name'})
        df['weight'] = df['weight'].astype('float')

        return df, div_yield, inc_date, net_expense_ratio

    def getCompanyOverview(self, ticker : list[str], wanted_attr : list[str] = ['']) -> dict:
        """
        Get the company overview as a dictionary
        """
        return
    
    def getCompanyOverviews(self, tickers : list[str], wanted_attr : list[str] = ['']) -> pd.DataFrame:
        """
        Get a dataframe filled with company overviews
        """
        return