import asyncio
import sys

import pyximport

pyximport.install()

from core.cross_cutting_concerns.logger.logger import init_inform_log, init_debug_log
from core.libraries.scraper.scraper import ScraperApi
from controller.is_yatirim.is_yatirim_controller import ISYatirimController

init_inform_log()
init_debug_log()

scrapers = ScraperApi()
controller = ISYatirimController()


async def main(arg: str):
    # Bist
    for code in scrapers.get_all_bist_company(arg):
        await controller.get_all_historical_data_async("bist_securities_hist_data",
                                                       ".E.BIST",
                                                       code,
                                                       2012,
                                                       9)
    # Foreign Currency
    # for code in ['USD/RUB', 'USD/CAD', 'USD/KWD', 'USD/BRL', 'USD/NOK', 'USD/COP', 'USD/CNH', 'USD/UYU',
    #              'USD/DKK', 'USD/DZD', 'USD/INR', 'USD/SAR', 'USD/SEK', 'USD/ZAR', 'USD/JOD', 'USD/KRW',
    #              'USD/AZN', 'USD/ARS', 'USD/BHD', 'USD/CHF', 'USD/CLP', 'USD/JPY', 'USD/QAR', 'USD/NZD',
    #              'USD/NOK', 'USD/COP', 'USD/CRC', 'USD/CSK', 'USD/EGP', 'USD/GEL', 'USD/GHS', 'USD/HKD',
    #              'USD/HRK', 'USD/HUF', 'USD/ILS', 'USD/IQD', 'USD/IRR', 'USD/ISK', 'USD/KZT', 'USD/LBP',
    #              'USD/LKR', 'USD/LYD', 'USD/MAD', 'USD/MDL', 'USD/MKD', 'USD/MZN', 'USD/MXN', 'USD/MYR',
    #              'USD/PHP', 'USD/PKR', 'USD/RSD', 'USD/SGD', 'USD/SYP', 'USD/TMT', 'USD/TWD', 'USD/UAH',
    #              'USD/UZS', 'GBP/USD', 'EUR/USD', 'EUR/AED', 'BTC/TRY', 'CHF/TRL', 'GBP/TRL', 'EUR/TRL',
    #              'USD/TRL']:
    #     await controller.get_all_historical_data_async("foreign_currency_hist_data",
    #                                                    "",
    #                                                    code,
    #                                                    2009,
    #                                                    1)
    #
    # # Emtia
    # for code in ['XAU/USD', 'XAG/USD', 'BRENT', 'XPD/USD', 'XPT/USD']:
    #     await controller.get_all_historical_data_async("emtia_hist_data",
    #                                                    "",
    #                                                    code,
    #                                                    2009,
    #                                                    9)


if __name__ == "__main__":
    asyncio.run(main(str(sys.argv[1])))
