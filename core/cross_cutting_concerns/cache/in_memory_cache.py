from expiringdict import ExpiringDict
cache = {}


def get_from_cache(dict_key: str, key: str):
    if dict_key in cache.keys():
        return cache[dict_key].get(key, None)
    else:
        cache[dict_key] = ExpiringDict(max_len=1000, max_age_seconds=86400)
        return cache[dict_key].get(key, None)


def set_cache(dict_key: str, key: str, value: any):
    if dict_key in cache.keys():
        cache[dict_key][key] = value
    else:
        cache[dict_key] = ExpiringDict(max_len=1000, max_age_seconds=86400)
        cache[dict_key][key] = value


def delete_cache(dict_key: str, cache_key: str):
    if dict_key in cache.keys():
        cache[dict_key].pop(cache_key)

