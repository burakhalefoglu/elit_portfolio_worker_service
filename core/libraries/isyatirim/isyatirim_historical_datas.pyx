import requests
from cpython.datetime cimport datetime, timedelta

cdef class IsYatirimHistoricalData:
    def get_all_bist_historical_data(self, str code,
                                     str  from_date_year,
                                     str  from_date_month,
                                     str  from_date_day,
                                     str  from_date_hour,
                                     str  to_date_year,
                                     str  to_month,
                                     str  to_day,
                                     str  to_hour,
                                     str  to_minute,
                                     str  from_date_minute) -> list:
        cdef int calculated_minute = 0
        cdef int to_calculated_minute = 0
        cdef datetime today
        cdef datetime second_day
        cdef list data = []

        try:
            calculated_minute = (int(from_date_hour) * 60 + int(from_date_minute))

            to_calculated_minute = (int(to_hour) * 60 + int(to_minute))

            if calculated_minute < 9 * 60 + 55:
                from_date_hour = "09"
                from_date_minute = "55"

            if to_calculated_minute > 18 * 60 + 5:
                to_hour = "18"
                to_minute = "05"

            today = datetime(int(from_date_year), int(from_date_month), int(from_date_day), int(from_date_hour),
                             int(from_date_minute), 0, 0)
            second_day = datetime(int(to_date_year), int(to_month), int(to_day), int(to_hour), int(to_minute), 0,
                                  0)
            day = today.weekday()

            if today > second_day:
                second_day = today + datetime.timedelta(days=1)
                to_date_year = second_day.year
                to_month = second_day.month
                to_day = second_day.day
                to_hour = second_day.hour
                to_minute = second_day.minute

            if day == 5:
                arranged_time_1 = today - timedelta(days=1)
                arranged_day = str(arranged_time_1.day)
                from_date_day = arranged_day

            if day == 6:
                arranged_time_2 = today - timedelta(days=2)
                arranged_day = str(arranged_time_2.day)
                from_date_day = arranged_day

            if (int(from_date_day) == 4) & (calculated_minute > 18 * 60):
                arranged_to_time = today + timedelta(days=3)
                arranged_to_day = str(arranged_to_time.day)
                to_day = arranged_to_day

            base_source = "https://www.isyatirim.com.tr/_Layouts/15/IsYatirim.Website/Common/ChartData.aspx/IndexHistoricalAll?period=1&"
            source = "from={fyear}{fmonth}{fday}{fhour}{fminute}00&to={tyear}{tmonth}{tday}{thour}{tminute}59&endeks={code}.E.BIST".format(
                fyear=from_date_year,
                fmonth=from_date_month,
                fday=from_date_day,
                fhour=from_date_hour,
                fminute=from_date_minute,
                tyear=to_date_year,
                tmonth=to_month,
                tday=to_day,
                thour=to_hour,
                tminute=to_minute,
                code=code)
            r = requests.get(base_source + source)
            req = r.json()
            data = req['data']
            return data
        except Exception as e:
            return []

    def get_isyatirim_from_to_historical_datas(self, str code,
                                               str from_date_year,
                                               str from_date_month,
                                               str from_date_day,
                                               str from_date_hour,
                                               str to_date_year,
                                               str to_month,
                                               str to_day,
                                               str to_hour,
                                               str to_minute,
                                               str from_date_minute):
        cdef list data = []
        base_source = "https://www.isyatirim.com.tr/_Layouts/15/IsYatirim.Website/Common/ChartData.aspx/IndexHistoricalAll?period=1&"
        source = "from={fyear}{fmonth}{fday}{fhour}{fminute}00&to={tyear}{tmonth}{tday}{thour}{tminute}59&endeks=".format(
            fyear=from_date_year,
            fmonth=from_date_month,
            fday=from_date_day,
            fhour=from_date_hour,
            fminute=from_date_minute,
            tyear=to_date_year,
            tmonth=to_month,
            tday=to_day,
            thour=to_hour,
            tminute=to_minute)

        r = requests.get(base_source + source + code)
        req = r.json()
        data = req['data']
        return data
