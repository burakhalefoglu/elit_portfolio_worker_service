import datetime
from typing import List, Any

import pandas as pd

from core.aspects.exception.exception_aspect import exception_aspect
from model.bist_historical_data import BistHistoricalData
from repository.databases.mongodb.mongodb_dal import MongodbDal


class BistSecuritiesHistoricalService:
    data_access = MongodbDal()

    @exception_aspect
    async def save_historical_data_async(self, code: str, date: datetime, data: List[Any]) -> Any:
        historical_data = []
        for i in range(len(data)):
            epoch_data_time = data[i][0]
            data_value = data[i][1]
            date_time = datetime.datetime.utcfromtimestamp(float(epoch_data_time) / 1000.)
            date_time_turkey = date_time + datetime.timedelta(hours=3)
            bist_historical_data = BistHistoricalData(
                code=code,
                value=data_value,
                date=date_time_turkey)
            historical_data.append(bist_historical_data.__dict__)
        if historical_data is [] or len(data) <= 5:
            raise Exception(str({"code": code, "date": date, "weekday": str(date.weekday()), "data": data}))

        historical_data_pd = pd.DataFrame(historical_data, columns=["code", "value", "date"])
        historical_data_pd = historical_data_pd.sort_values(by="date")
        historical_dict = historical_data_pd.to_dict('records')
        await self.data_access.add_many_async("bist_securities_historical_datas",
                                              historical_dict)
