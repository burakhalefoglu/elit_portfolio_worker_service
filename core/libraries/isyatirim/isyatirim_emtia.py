import datetime
from numpy import float64
import requests
import pandas as pd
import lxml


class IsYatirimEmtia:

    async def get_emtias_name_and_codes(self) -> pd.DataFrame:
        source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
        emtia_list = ['XAU/USD', 'XAG/USD', 'BRENT', 'XPD/USD', 'XPT/USD']
        emtia_data_list = []
        for emtia in emtia_list:
            r = requests.get(source + emtia)
            emtia_data = r.json()[0]
            emtia_data_list.append(emtia_data)

        df = pd.DataFrame(emtia_data_list)
        df = df.rename(columns={'c': 'code', 'description': 'title', 'last': 'price'})
        weight_type = ['ons', 'ons', 'brend', '13 gram Truva', '13 gram Truva']
        df['weight_type'] = weight_type
        pd.set_option('display.precision', 16)
        return df[['code', 'title', 'weight_type']]

    async def get_emtia_price(self, code: str):
        source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
        r = requests.get(source + code)
        emtia_data_price = r.json()[0]['last']
        emtia_data_price = float64(emtia_data_price)
        usd_tl = self.__get_usd_tl_currency()
        emtia_tl = emtia_data_price*usd_tl
        pd.set_option('display.precision', 16)
        return emtia_tl



    async def __get_usd_tl_currency(self):
       source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
       code =  'USD/TRL' 
       r = requests.get(source + code)
       usd_tl_price = r.json()[0]['last']
       usd_tl_price = float64(usd_tl_price)
       pd.set_option('display.precision', 16)
       return usd_tl_price

    async def get_current_gold_usd_price(self):
        source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
        code = "XAU/USD"
        r = requests.get(source + code)
        gold_price = r.json()[0]['last']
        gold_price = float64(gold_price)
        pd.set_option('display.precision', 16)
        return gold_price


    async def get_current_siver_usd_price(self):
        source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
        code = "XAG/USD"
        r = requests.get(source + code)
        silver_price = r.json()[0]['last']
        silver_price = float64(silver_price)
        pd.set_option('display.precision', 16)
        return silver_price

