import asyncio

import pyximport

pyximport.install()

from core.cross_cutting_concerns.logger.logger import init_inform_log, init_debug_log
from core.libraries.scraper.scraper import ScraperApi
from controller.is_yatirim.is_yatirim_controller import ISYatirimController

init_inform_log()
init_debug_log()

scrapers = ScraperApi()
controller = ISYatirimController()


async def main():
    tasks = [asyncio.create_task(controller.get_all_historical_data_async(code))
             for code in scrapers.get_all_bist_company()]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
