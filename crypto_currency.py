import pyximport
pyximport.install()
import pandas as pd
from core.libraries.cryptomd.cyripto_currency import CmcScraperCryptoApi
import requests
import asyncio
from repository.mongodb.mongodb_dal import MongodbDal



cmc = CmcScraperCryptoApi()


async def save_cryptos_hist_data():

    df = pd.read_json("crypto_currency.json")

    for data in df.to_dict("records"):
        df_crypto = await cmc.get_crypto_currency_all_time(data.code)
        df_dict = df_crypto.to_dict('records')
        if len(df_dict) == 0:
            data['status']=False
            await data_access.add_async("crypto_currency_metadata",
                                        data)
            continue

        data['status'] = True
        await data_access.add_async("crypto_currency_metadata",
                                    data)
        await data_access.add_many_async("crypto_currency_hist_data",
                                         df_dict)


if __name__ == "__main__":
    asyncio.run(save_cryptos_hist_data())