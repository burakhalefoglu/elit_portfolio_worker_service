import pandas as pd

from core.libraries.investpy.stocks import get_stock_historical_data, get_stock_recent_data


class InvestpyApi:

    async def get_universal_investpy_companies_recent_stock_price(self, code: str, country: str) -> pd.DataFrame:
        df = get_stock_recent_data(stock=code, country=country)
        return df.iloc[-1:]

    async def get_universal_investpy_companies_history_stock_price(self, code: str, country: str,
                                                             from_day: str, from_month: str, from_year: str,
                                                             to_day: str, to_month: str, to_year: str) -> pd.DataFrame:
        df = get_stock_historical_data(stock=code,
                                       country=country,
                                       from_date=f'{from_day}/{from_month}/{from_year}',
                                       to_date=f'{to_day}/{to_month}/{to_year}')
        return df
