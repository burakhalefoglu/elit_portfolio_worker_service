import logging

from colorama import Fore, Back
from colorama import init

init()


class CustomFormatter(logging.Formatter):
    format = "%(asctime)s - %(name)s - %(levelname)s- (%(filename)s:%(lineno)d)" \
             "[func: %(funcName)s] -->> message: %(message)s"

    FORMATS = {
        logging.DEBUG: Fore.CYAN + format + Fore.RESET,
        logging.INFO: Fore.GREEN + format + Fore.RESET,
        logging.WARNING: Fore.YELLOW + format + Fore.RESET,
        logging.ERROR: Fore.RED + format + Fore.RESET,
        logging.CRITICAL: Back.RED + format + Fore.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
