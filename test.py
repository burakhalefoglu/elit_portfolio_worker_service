import asyncio
from datetime import datetime, timedelta

import pyximport

pyximport.install()

from core.libraries.tefas.pension_fund_crawler import PensionFundsCrawler
from core.libraries.tefas.securities_mutual_funds_crawler import SecuritiesMutualFundsCrawler
from repository.mongodb.mongodb_dal import MongodbDal


async def start_securities_mutual_funds():
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    data_access = MongodbDal()
    while True:
        new_list = []
        securities_mutual_funds_historical_data = SecuritiesMutualFundsCrawler().fetch_historical_data(
            start=start_date,
            end=end_date)
        securities_mutual_funds_list = securities_mutual_funds_historical_data.to_dict('records')
        print("securities_mutual_funds_historical_data: ",
              len(securities_mutual_funds_list))

        for el in securities_mutual_funds_list:
            el["date"] = datetime.combine(el["date"], datetime.min.time())
            new_list.append(el)

        await data_access.add_many_async("securities_mutual_funds_hist_data",
                                         new_list)

        if start_date.year < 2017:
            break
        start_date = start_date - timedelta(days=90)
        end_date = end_date - timedelta(days=90)


async def start_pension_funds():
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    data_access = MongodbDal()
    while True:
        new_list = []
        pension_funds_crawler_data = PensionFundsCrawler().fetch_historical_data(
            start=start_date,
            end=end_date)
        pension_data_list = pension_funds_crawler_data.to_dict('records')
        print("pension_funds_crawler_data: ", len(pension_data_list))
        for el in pension_data_list:
            el["date"] = datetime.combine(el["date"], datetime.min.time())
            new_list.append(el)
        await data_access.add_many_async("pension_funds_hist_data",
                                         new_list)

        if start_date.year < 2017:
            break
        start_date = start_date - timedelta(days=90)
        end_date = end_date - timedelta(days=90)


if __name__ == '__main__':
    # asyncio.run(start_securities_mutual_funds())
    asyncio.run(start_pension_funds())
