import requests
import datetime
import pandas as pd


class MarketData():
    """
    Utility class for collecting market information
    """
    def __init__(self, api_key : str, date_range : tuple[datetime.date, datetime.date]):
        
        self.base_url = "https://www.alphavantage.co/query?"
        
        self.api_key = api_key
        self.date_range = date_range
    
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

        assert (dateCol in df), f"{dateCol} does not exist in the passed df, try agin"

        df[dateCol] = pd.to_datetime(df[dateCol], errors='raise')
   
        options = [
            (doYear, 'year', df[dateCol].dt.year),
            (doMonth,'month', df[dateCol].dt.month),
            (doDay, 'day', df[dateCol].dt.day),
            (doHour, 'hour', df[dateCol].dt.hour),
            (doMinute, 'minute', df[dateCol].dt.minute),
            (doSecond, 'second', df[dateCol].dt.second)
            (doEpoch, 'epoch', df[dateCol].astype('int64') // 10**9)
        ]
        
        for flag, col, value in options:
            if flag:
                df[col] = value

        if not inplace:
            return df

        return None
    
    def getPxAction(self, ticker : str, interval : str = '5min') -> pd.DataFrame:
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

        #the api call
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}&apikey={self.api_key}&extended_hours=false'

        r = requests.get(url)
        data = r.json()[f'Time Series ({interval})']

        df = pd.DataFrame.from_dict(data).T
        df = df.apply(pd.to_numeric).reset_index()
        df = df.rename(columns={'1. open' : 'open',
                '2. high' : 'high',
                '3. low' : 'low',
                '4. close' :'close',
                '5. volume' : 'volume',
                'index' : 'datetime'})
        
        self.datetimeDecompose(df, 'datetime')
        
        df = (df
            .set_index('epoch')
            .reindex(columns=[ 'year', 'month', 'day', 'hour', 'minute', 
                        'open', 'high', 'low', 'close']))

        return df
    
data = MarketData('demo', ())
df = data.getPxAction('IBM')
print(df)