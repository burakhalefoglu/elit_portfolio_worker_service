import datetime
from numpy import float64
import requests
import pandas as pd
import lxml

class IsYatirimForeignCurrency:


    async def __convert_currency_each_other(self, currency_data):
        currency_split = currency_data['c'].split('/')
        currency_convert_data = {}
        currency_convert_data['c'] = "{codelast}/{codefirst}".format(codelast=currency_split[1], codefirst=currency_split[0])
        currency_convert_data['last'] = float64(1)/float64(currency_data['last'])
        description_split = currency_data['description'].split('/')
        currency_convert_data['description'] = "{desclast}/{descfirst}".format(desclast=description_split[1], descfirst=description_split[0])
        return currency_convert_data


    async def __get_all_current_foreign_currency(self):

        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        currency_with_usd_code_list = [ 'USD/RUB', 'USD/CAD', 'USD/KWD', 'USD/BRL', 'USD/NOK', 'USD/COP', 'USD/CNH', 'USD/UYU',
                                        'USD/DKK', 'USD/DZD', 'USD/INR', 'USD/SAR', 'USD/SEK', 'USD/ZAR', 'USD/JOD', 'USD/KRW',
                                        'USD/AZN', 'USD/ARS', 'USD/BHD', 'USD/CHF', 'USD/CLP', 'USD/JPY', 'USD/QAR', 'USD/NZD', 
                                        'USD/NOK', 'USD/COP', 'USD/CRC', 'USD/CSK', 'USD/EGP', 'USD/GEL', 'USD/GHS', 'USD/HKD',
                                        'USD/HRK', 'USD/HUF', 'USD/ILS', 'USD/IQD', 'USD/IRR', 'USD/ISK', 'USD/KZT', 'USD/LBP',
                                        'USD/LKR', 'USD/LYD', 'USD/MAD', 'USD/MDL', 'USD/MKD', 'USD/MZN', 'USD/MXN', 'USD/MYR',
                                        'USD/PHP', 'USD/PKR', 'USD/RSD', 'USD/SGD', 'USD/SYP', 'USD/TMT', 'USD/TWD', 'USD/UAH',
                                        'USD/UZS']

        currency_list = []
  
        for currency in currency_with_usd_code_list:
            r = requests.get(source + currency)
            currency_data = r.json()[0]
            currency_data['last'] = float64(currency_data['last'])
            currency_list.append(currency_data)

        gbp_and_eur_list =self.__calculate_gbp_and_eur_currency()
        aed_dict = self.__calculate_usd_aed_currency()
        btc_dict = self.__calculate_usd_btc_currency()
        aed_btc_list = [aed_dict, btc_dict]
        gbp_and_eur_list.extend(aed_btc_list)

        currency_list.extend(gbp_and_eur_list)
        df = pd.DataFrame(currency_list)
        df = df.rename(columns = {'c':'code', 'last': 'price', 'description': 'title'})
        df_final = df[['code', 'price', 'title']]

        pd.set_option('display.precision', 16)

        return df_final


    def __calculate_gbp_and_eur_currency(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        currency_toward_usd_code_list = ['GBP/USD', 'EUR/USD']

        converted_currency_list = []
        for currency in currency_toward_usd_code_list:
            r = requests.get(source + currency)
            currency_data = r.json()[0]
            currency_data['last'] = float64(currency_data['last'])

            currency_convert_data = self.__convert_currency_each_other(currency_data)
            converted_currency_list.append(currency_convert_data)
        pd.set_option('display.precision', 16)

        return converted_currency_list



    def __calculate_usd_aed_currency(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        currency_list = ['EUR/AED', 'EUR/USD']
        currency_data_list = []
        r = requests.get(source)
        for currency in currency_list:
            r = requests.get(source + currency)
            currency_data = r.json()[0]
            currency_data['last'] = float64(currency_data['last'])
            currency_data_list.append(currency_data['last'])
        result = currency_data_list[0]/currency_data_list[1]
        eur_aed_dict = {}
        eur_aed_dict['c'] = "USD/AED"
        eur_aed_dict['last'] = result
        eur_aed_dict['description'] = 'US Dollar / UAE Dirham'
        return eur_aed_dict


    def __calculate_usd_btc_currency(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        currency_list = ['USD/TRL', 'BTC/TRY']
        currency_data_list = []
        for currency in currency_list:
            r = requests.get(source + currency)
            currency_data = r.json()[0]
            currency_data['last'] = float64(currency_data['last'])
            currency_data_list.append(currency_data['last'])
        result = currency_data_list[0]/currency_data_list[1]
        usd_btc_dict = {}
        usd_btc_dict['c'] = "USD/BTC"
        usd_btc_dict['last'] = result
        usd_btc_dict['description'] = 'US Dollar / Bitcoin'
        return usd_btc_dict



    def __get_current_foreign_currency_TurkishLira(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        currency_with_tl_code_list = ['BTC/TRY', 'CHF/TRL', 'GBP/TRL', 'EUR/TRL', 'USD/TRL']
        currency_with_tl_list = []

        for currency in currency_with_tl_code_list:
             r = requests.get(source + currency)
             currency_data = r.json()[0]
             currency_data['last'] = float64(currency_data['last'])
             currency_with_tl_list.append(currency_data)

        df = pd.DataFrame(currency_with_tl_list)
        df = df.rename(columns = {'c':'code'})
        df_final = df[['code', 'last', 'description']]
        pd.set_option('display.precision', 16)
        return df_final



    def __calculate_currency(self, code: str):   
        codes = code.split("/")
        code1 = "USD/" + codes[0]
        code2 = "USD/" + codes[1]
        return code2 / code1



    def calculate_current_tl_currency(self, param: str):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        tl = 'USD/TRL'
        r = requests.get(source + tl)
        currency_data = r.json()[0]
        currency_data['last'] = float64(currency_data['last'])
        foreign_currencies_df = self.__get_all_current_foreign_currency()
        query =  'USD/' + param
        usd_price = foreign_currencies_df.loc[foreign_currencies_df['code'] == query]['price'].values[0]
        return currency_data['last']/usd_price


    def get_current_usd_try_price(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        tl = 'USD/TRL'
        r = requests.get(source + tl)
        currency_data = r.json()[0]
        currency_data['last'] = float64(currency_data['last'])
        return currency_data['last']


    def get_current_eur_try_price(self):
        source = 'https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks='
        tl = 'EUR/TRL'
        r = requests.get(source + tl)
        currency_data = r.json()[0]
        currency_data['last'] = float64(currency_data['last'])
        return currency_data['last']



    def get_foreign_currency_codes(self):
        currency_df = self.__get_all_current_foreign_currency()
        return currency_df[['code', 'title']]



    def get_current_foreign_currency_by_code(self, code: str):

        source = "https://www.isyatirim.com.tr/_layouts/15/Isyatirim.Website/Common/Data.aspx/OneEndeks?endeks="
        r = requests.get(source + code)
        currency_data = r.json()[0]
        currency_data['last'] = float64(currency_data['last'])
        return currency_data['last']


    
