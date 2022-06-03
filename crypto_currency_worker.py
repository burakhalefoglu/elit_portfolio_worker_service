import pyximport
pyximport.install()
import pandas as pd
from core.libraries.cryptomd.cyripto_currency import CmcScraperCryptoApi
import asyncio
from repository.mongodb.mongodb_dal import MongodbDal

class CryptoCurrencyWorker:
    cmc = CmcScraperCryptoApi()
    data_access = MongodbDal()

    async def crypt_currrency_worker_service(self):
        crypto_table = await self.data_access.get_all_async("crypto_currency_metadata")
        crypto_list = []
        try:
            for index, data in enumerate(crypto_table):
                df_crypto = await self.cmc.get_yesterday_crypto_currency(data["code"])
                df_crypto["Code"] = data["code"]
                df_crypto["Title"] = data["title"]
                df_crypto.drop("Market Cap", axis=0, inplace=True)
                df_dict = df_crypto.to_dict()
                crypto_list.append(df_dict)
                print(index, data["code"])
            await self.data_access.add_many_async("crypto_currency_hist_data",
                                                crypto_list)
        except Exception as e:
            print(e)    



c = CryptoCurrencyWorker()
asyncio.run(c.crypt_currrency_worker_service())