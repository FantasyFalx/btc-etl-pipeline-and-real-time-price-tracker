# Standard libraries
# 3rd party
import yfinance as yf
# Custom modules



class YFinanceManager:
    def __init__(self):
        self.investing_object: yf.Ticker = None


    def set_investing_object(self, ticker: str):
        self.investing_object = yf.Ticker(ticker)


