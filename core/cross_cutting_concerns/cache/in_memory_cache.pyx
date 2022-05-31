from expiringdict import ExpiringDict

cdef dict cache = {}

def get_from_cache(str dict_key, str key):
    if dict_key in cache.keys():
        return cache[dict_key].get(key, None)
    else:
        cache[dict_key] = ExpiringDict(max_len=1000, max_age_seconds=86400)
        return cache[dict_key].get(key, None)


def set_cache(str dict_key, str key, object value):
    if dict_key in cache.keys():
        cache[dict_key][key] = value
    else:
        cache[dict_key] = ExpiringDict(max_len=1000, max_age_seconds=86400)
        cache[dict_key][key] = value


def delete_cache(str dict_key, str cache_key):
    if dict_key in cache.keys():
        cache[dict_key].pop(cache_key)

