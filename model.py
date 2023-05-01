import yfinance as yf
from prophet import Prophet
import pandas as pd

class Model:
    def __init__(self):
        self.START = "2015-01-01"
    
    def load_data(self, ticker, end) -> pd.DataFrame:
        data = yf.download(ticker, self.START, end)
        data.reset_index(inplace=True)
        return data
    
    def train(self, data) -> pd.DataFrame:
        df_train = data[['Date','Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        return df_train

    def predict(self, df_train, period=60) -> pd.DataFrame:
        m = Prophet()
        m.fit(df_train)
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)
        # print(forecast.tail(period))
        return forecast[['ds','yhat']].tail(period)
