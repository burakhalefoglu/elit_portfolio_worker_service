import requests


class IsYatirimBist:
    async def get_current_securities_value_by_code(self, code: str) -> float:
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        r = requests.get(
            source + code + '.E.BIST')
        result = r.json()
        return result[0]['last']
