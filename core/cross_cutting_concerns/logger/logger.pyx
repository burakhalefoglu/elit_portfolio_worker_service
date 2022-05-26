import json
import logging
import logging.handlers
import os

from dotenv import load_dotenv

from core.cross_cutting_concerns.logger.handlers.console_handler import CustomFormatter
from core.cross_cutting_concerns.logger.handlers.email_handler import SSLSMTPHandler
from core.cross_cutting_concerns.logger.handlers.mongodb_handler import MongoHandler

load_dotenv()
mongodb_connection = os.getenv('MONGODB')

mail_host = os.getenv('MAIL_HOST')
mail_port = os.getenv('MAIL_PORT')
sender = os.getenv('EMAIL_SENDER')
pwd = os.getenv('PASSWORD')
to_address = os.getenv('TO_ADDRESS')
subject = os.getenv('SUBJECT')

debug_logger = logging.getLogger("Debug Log")
inform_logger = logging.getLogger("Inform Log")


def init_debug_log():
    #  create debug_logger
    debug_logger.setLevel(logging.DEBUG)

    # Console debug_logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())

    # Create equivalent mail handler
    mail_handler = SSLSMTPHandler(mailhost=(mail_host, int(mail_port)),
                                  fromaddr=sender,
                                  toaddrs=json.loads(to_address),
                                  subject=subject,
                                  credentials=(sender, pwd), )

    # Set the email format
    mail_handler.setFormatter(logging.Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    mail_handler.setLevel(logging.ERROR)

    # add handlers
    debug_logger.addHandler(MongoHandler.to(host=mongodb_connection, collection='logs'))
    debug_logger.addHandler(ch)
    debug_logger.addHandler(mail_handler)


def init_inform_log():
    # create inform_log
    inform_logger.setLevel(logging.DEBUG)

    # mongodb debug_logger
    inform_logger.addHandler(MongoHandler.to(host=mongodb_connection, collection='logs'))
