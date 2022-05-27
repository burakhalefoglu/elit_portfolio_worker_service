import requests

cdef class IsYatirimHistoricalData:
    def get_isyatirim_from_to_historical_datas(self, str code,
                                               str query,
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
        try:
            base_source = "https://www.isyatirim.com.tr/_Layouts/15/IsYatirim.Website/Common/ChartData.aspx/IndexHistoricalAll?period=1440&"
            source = "from={fyear}{fmonth}{fday}{fhour}{fminute}00&to={tyear}{tmonth}{tday}{thour}{tminute}59&endeks={code}{query}".format(
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
                code=code,
                query=query)

            r = requests.get(base_source + source)
            req = r.json()
            data = req['data']
            return data
        except Exception as e:
            return []
