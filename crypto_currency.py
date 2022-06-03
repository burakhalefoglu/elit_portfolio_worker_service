import pyximport
pyximport.install()
import pandas as pd
from core.libraries.cryptomd.cyripto_currency import CmcScraperCryptoApi
import asyncio
from repository.mongodb.mongodb_dal import MongodbDal




async def save_cryptos_hist_data():
    cmc = CmcScraperCryptoApi()
    data_access = MongodbDal()
    df = pd.read_json("crypto_currency.json")
    sayac = 0
    for index ,data in enumerate(df.to_dict("records")):
        try:
            sayac = 1 + index
            df_crypto = await cmc.get_crypto_currency_all_time(data["code"])
            df_crypto["Code"] = data["code"]
            df_crypto["Title"] = data["title"]
            df_crypto.drop("Market Cap", axis=1, inplace=True)
            df_dict = df_crypto.to_dict('records')
            if len(df_dict) == 0:
                continue
            print(sayac, data["code"])
            data['status'] = True
            await data_access.add_async("crypto_currency_metadata",
                                        data)
            await data_access.add_many_async("crypto_currency_hist_data",
                                            df_dict)
            sayac = sayac + 1
        except Exception as e:
            data['status']=False
            await data_access.add_async("crypto_currency_metadata",
                                            data)
            print("veri yok")
        
if __name__ == "__main__":
    asyncio.run(save_cryptos_hist_data())