import pyximport

from core.cross_cutting_concerns.logger.logger import init_debug_log, init_inform_log

pyximport.install()
import asyncio
import threading

from controller.is_yatirim.is_yatirim_controller import ISYatirimController

init_inform_log()
init_debug_log()

# from core.utilities.toolkit.thread_job import ThreadJob
event = threading.Event()

# Workers
controller = ISYatirimController()

# Define worker
# k = ThreadJob(main, event, 2)


# Start workers
if __name__ == '__main__':
    # k.start()
    asyncio.run(controller.get_all_historical_data_async())
