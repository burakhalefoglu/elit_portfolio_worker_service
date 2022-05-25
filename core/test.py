import asyncio
from datetime import timedelta, datetime

import pyximport

pyximport.install()
from controller.is_yatirim.is_yatirim_controller import date_obj_to_str
from core.libraries.isyatirim.isyatirim_historical_datas import IsYatirimHistoricalData
from service.bist_securities_historical_service import BistSecuritiesHistoricalService

isyatirim_historical_datas = IsYatirimHistoricalData()
bist_service = BistSecuritiesHistoricalService()

# -----Bu yabancı paralar ve emtialar için kullanılacak-----
# for i in ["USD/TRL"]:
#     d = isyatirim_historical_datas.get_isyatirim_from_to_historical_datas(i, "2013", "06", "03", "09", "2022", "05",
#                                                                           "20", "22", "50", "00")
#
#     bist_service.save_historical_data_async(i, d)

today = datetime.now()

while True:
    hist_data = isyatirim_historical_datas.get_all_bist_historical_data(code="AEFES",
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

    if len(hist_data) == 0:
        # log to csv
        continue

    asyncio.run(bist_service.save_historical_data_async(code="AEFES",
                                                        data=hist_data))
    today = today - timedelta(days=1)

