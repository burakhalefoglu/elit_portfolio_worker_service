from datetime import datetime, timedelta

from core.aspects.exception.exception_aspect import exception_aspect
from core.libraries.isyatirim import isyatirim_historical_datas
from service.bist_securities_historical_service import BistSecuritiesHistoricalService


class ISYatirimController:
    is_yatirim_data_sources = isyatirim_historical_datas.IsYatirimHistoricalData()
    bist_securities_hist_services = BistSecuritiesHistoricalService()

    @exception_aspect
    async def get_all_historical_data_async(self, code: str):
        min_date = datetime(2012, 9, 14, 9, 0)
        today = datetime.now()
        counter = 0
        while True:
            hist_data = self.is_yatirim_data_sources.get_all_bist_historical_data(code=code,
                                                                                  from_date_year=str(
                                                                                      today.year),
                                                                                  from_date_month=date_obj_to_str(
                                                                                      today.month),
                                                                                  from_date_day=date_obj_to_str(
                                                                                      today.day),
                                                                                  from_date_hour="09",
                                                                                  from_date_minute="00",
                                                                                  to_date_year=str(today.year),
                                                                                  to_month=date_obj_to_str(
                                                                                      today.month),
                                                                                  to_day=date_obj_to_str(today.day),
                                                                                  to_hour="23",
                                                                                  to_minute="59"
                                                                                  )
            if today < min_date:
                break
            if len(hist_data) <= 5:
                counter = counter + 1
            else:
                counter = 0

            if counter >= 20:
                raise Exception(str({"code": code, "resaon": "üst üste çok veri yok"}))

            await self.bist_securities_hist_services.save_historical_data_async(code=code,
                                                                                date=today,
                                                                                data=hist_data)

            today = today - timedelta(days=1)


def date_obj_to_str(element: int) -> str:
    if element <= 9:
        return "0" + str(element)
    return str(element)
