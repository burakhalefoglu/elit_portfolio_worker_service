from datetime import datetime, timedelta

from core.aspects.exception.exception_aspect import exception_aspect
from core.libraries.isyatirim import isyatirim_historical_datas
from service.bist_securities_historical_service import BistSecuritiesHistoricalService


class ISYatirimController:
    is_yatirim_data_sources = isyatirim_historical_datas.IsYatirimHistoricalData()
    bist_securities_hist_services = BistSecuritiesHistoricalService()

    @exception_aspect
    async def get_all_historical_data_async(self, table: str,
                                            query: str,
                                            code: str,
                                            min_data_year: int,
                                            min_data_mount: int):
        min_date = datetime(year=min_data_year, month=min_data_mount, day=1)
        today = datetime.now()
        count = 0
        while True:
            hist_data = self.is_yatirim_data_sources.get_isyatirim_from_to_historical_datas(code=code,
                                                                                            query=query,
                                                                                            from_date_year=str(
                                                                                                today.year),
                                                                                            from_date_month=date_obj_to_str(
                                                                                                today.month),
                                                                                            from_date_day=date_obj_to_str(
                                                                                                today.day),
                                                                                            from_date_hour="00",
                                                                                            from_date_minute="00",
                                                                                            to_date_year=str(
                                                                                                today.year),
                                                                                            to_month=date_obj_to_str(
                                                                                                today.month),
                                                                                            to_day=date_obj_to_str(
                                                                                                today.day),
                                                                                            to_hour="23",
                                                                                            to_minute="59"
                                                                                            )
            if today < min_date:
                break
            print("code", code, hist_data)
            result = await self.bist_securities_hist_services.save_historical_data_async(table=table,
                                                                                         code=code,
                                                                                         date=today,
                                                                                         data=hist_data)
            if result != {}:
                count = count + 1
                result["count"] = count
                await self.bist_securities_hist_services.save_last_stayed("last_date_with_codes", result)

            today = today - timedelta(days=1)
        count = 0


def date_obj_to_str(element: int) -> str:
    if element <= 9:
        return "0" + str(element)
    return str(element)
