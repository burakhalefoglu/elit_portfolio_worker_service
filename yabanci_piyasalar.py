import asyncio

import pyximport

pyximport.install()

from repository.mongodb.mongodb_dal import MongodbDal
from core.libraries.investpy.get_universal_companies_stocks_prices import InvestpyApi
from core.libraries.scraper.scraper import ScraperApi


# (df["country"] == "turkey") (df["country"] == "united states") | (
#                     df["country"] == "france") | (df["country"] == "spain") | (
#                     df["country"] == "united kingdom") |  (
#                     df["country"] == "germany") | (df["country"] == "italy") |

async def fetch_investpy_historical_data(country: str):
    investpy_api = InvestpyApi()
    scraper = ScraperApi()
    data_access = MongodbDal()
    df_list = await scraper.get_universal_investpy_company_list()
    code_list = df_list[df_list["country"] == country]["symbol"].to_list()
    for code in code_list:
        try:
            df = await investpy_api.get_universal_investpy_companies_history_stock_price(code=code,
                                                                                         country="united states",
                                                                                         from_day="01",
                                                                                         from_month="01",
                                                                                         from_year="1900",
                                                                                         to_day="31",
                                                                                         to_month="05",
                                                                                         to_year="2022")
            df["code"] = code
            df["country"] = country.replace(" ", "_")
            df.drop('Volume', axis=1, inplace=True)
            df_list = df.to_dict('records')

            await data_access.add_many_async("securities_hist_data",
                                             df_list)
            print(code)
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)




if __name__ == "__main__":
    asyncio.run(fetch_investpy_historical_data("united states"))
    asyncio.run(fetch_investpy_historical_data("turkey"))
    asyncio.run(fetch_investpy_historical_data("united kingdom"))


