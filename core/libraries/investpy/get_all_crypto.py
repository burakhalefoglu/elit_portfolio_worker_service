from core.libraries.investpy.crypto import get_crypto_recent_data, get_cryptos_list


class InvestpyApiCrypto:

    def get_crypto_currencies_list(self):
        crypo_list = get_cryptos_list()
        return crypo_list

    def get_recent_crypto_price(self, code: str):
        df = get_crypto_recent_data(crypto=code)
        return df
