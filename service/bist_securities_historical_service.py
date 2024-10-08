import datetime
from typing import List, Any

import pandas as pd
from repository.mongodb.mongodb_dal import MongodbDal

from model.bist_historical_data import BistHistoricalData


class BistSecuritiesHistoricalService:
    data_access = MongodbDal()

    async def get_by_filter(self, table: str, filters: dict) -> dict:
        return await self.data_access.get_list_by_filter_async(table,
                                                               filters)

    async def save_last_stayed(self, table: str, model: dict):
        result = await self.data_access.get_by_filter_async(table, {"code": model["code"]})
        if result is None:
            await self.data_access.add_async(table, model)
            return

        await self.data_access.update_async(table,
                                            {"code": model["code"]},
                                            {"date": model["date"],
                                             "count": model["count"]})

    async def save_historical_data_async(self, table: str, code: str, date: datetime, data: List[Any]) -> Any:
        historical_datas = []

        if len(data) == 0:
            return {}

        for i in range(len(data)):
            epoch_data_time = data[i][0]
            data_value = data[i][1]
            date_time = datetime.datetime.utcfromtimestamp(float(epoch_data_time) / 1000.)
            date_time_turkey = date_time + datetime.timedelta(hours=3)
            bist_historical_data = BistHistoricalData(
                code=code,
                value=data_value,
                date=date_time_turkey)
            historical_datas.append(bist_historical_data.__dict__)
        historical_data_pd = pd.DataFrame(historical_datas, columns=["code", "value", "date"])
        historical_data_pd = historical_data_pd.sort_values(by="date")

        historical_dict = historical_data_pd.to_dict('records')
        print(historical_dict)
        await self.data_access.add_many_async(table,
                                              historical_dict)
        return {"code": code, "date": date}
