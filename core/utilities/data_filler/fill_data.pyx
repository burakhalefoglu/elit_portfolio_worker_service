from cpython.datetime cimport timedelta

def fill_data_by_dates(list data) -> list:
    cdef list new_data = []
    cdef int i
    cdef dict now_element
    cdef dict previus_element
    cdef float result
    for i, _ in enumerate(data):
        now_element = data[i]
        previus_element = data[i - 1]
        if i == 0:
            new_data.append(now_element)
            continue
        result = (now_element["date"] - previus_element["date"]).total_seconds()
        if result == 1 or (now_element["date"].weekday()
                           == 0 and now_element["date"].hour == 9 and now_element[
                               "date"].minute == 55):
            new_data.append(now_element)
            continue

        for n in range(1, int(result)):
            prev_new_date = previus_element["date"] + timedelta(minutes=n)
            if prev_new_date.weekday() == 0 and \
                    prev_new_date.hour <= 9 and \
                    prev_new_date.minute <= 54:
                continue
            new_data.append({"code": previus_element["code"],
                             "date": prev_new_date,
                             "value": previus_element["value"]})
    print(new_data)
    return new_data
