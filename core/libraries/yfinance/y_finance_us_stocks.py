import yfinance as yf


class Y_FinanceApi:

    def get_us_companies_current_price(self, code: str):
        data = yf.Ticker(code)
        todays_data = data.history(period='1d')
        return todays_data['Close'][0]
  
     






# price = stock.info['regularMarketPrice']
# todays_data = data.history(period='1d')
# return todays_data["Close"][0]



