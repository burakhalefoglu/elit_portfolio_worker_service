from datetime import datetime, timedelta

from core.libraries.isyatirim import isyatirim_historical_datas
from core.libraries.scraper.scraper import ScraperApi
from service.bist_securities_historical_service import BistSecuritiesHistoricalService


class ISYatirimController:
    is_yatirim_data_sources = isyatirim_historical_datas.IsYatirimHistoricalData()
    scraper = ScraperApi()
    bist_securities_hist_services = BistSecuritiesHistoricalService()

    async def get_all_historical_data_async(self):
        for code in self.scraper.get_all_bist_company():
            today = datetime.now()
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
                min_date = datetime(2012, 9, 14, 9, 0)
                if today < min_date:
                    break

                await self.bist_securities_hist_services.save_historical_data_async(code=code,
                                                                                    date=today,
                                                                                    data=hist_data)
                today = today - timedelta(days=1)


def date_obj_to_str(element: int) -> str:
    if element < 9:
        return "0" + str(element)
    return str(element)
