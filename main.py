import pyximport
from rq import Worker, Queue

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
listen = ['high']

# Start workers
if __name__ == '__main__':
    asyncio.run(controller.get_all_historical_data_async())
    worker = Worker(map(Queue, listen))
    worker.work()
