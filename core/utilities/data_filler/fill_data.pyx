import pandas as pd
from cpython.datetime cimport timedelta

def fill_data_by_dates(list data) -> pd.DataFrame:
    cdef list new_data = []
    cdef int i
    cdef dict now_element
    cdef dict previus_element
    cdef float difference_minute
    for i, _ in enumerate(data):
        now_element = data[i]
        previus_element = data[i - 1]
        difference_minute = (now_element["date"] - previus_element["date"]).total_seconds() / 60

        if i == 0 or difference_minute == 1 or (now_element["date"].weekday()
                           == 0 and now_element["date"].hour == 9 and now_element[
                               "date"].minute == 55):
            new_data.append(now_element)
            continue

        for n in range(int(difference_minute)):
            prev_new_date = previus_element["date"] + timedelta(minutes=n)
            if prev_new_date.hour == 18 and prev_new_date.minute >= 10:
                continue

            if prev_new_date.hour >= 9 and prev_new_date.hour < 19:
                new_data.append({"code": previus_element["code"],
                                 "date": prev_new_date,
                                 "value": previus_element["value"]})

    new_df = pd.DataFrame(new_data).sort_values(by="date")
    df.to_dict('records')
    return new_df
