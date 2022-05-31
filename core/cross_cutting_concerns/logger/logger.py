import email
import json
import logging
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from mongolog.handlers import MongoHandler
from colorama import init
from colorama import Fore, Back
import logging.handlers

init()
load_dotenv()
mongodb_connection = os.getenv('MONGODB')

mail_host = os.getenv('MAIL_HOST')
mail_port = os.getenv('MAIL_PORT')
sender = os.getenv('EMAIL_SENDER')
pwd = os.getenv('PASSWORD')
to_address = os.getenv('TO_ADDRESS')
subject = os.getenv('SUBJECT')


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


debug_logger = logging.getLogger("Debug Log")
inform_logger = logging.getLogger("Inform Log")


def init_debug_log():
    #  create debug_logger
    debug_logger.setLevel(logging.DEBUG)

    # Console debug_logger
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(CustomFormatter())

    # email debug_logger
    class SSLSMTPHandler(logging.handlers.SMTPHandler):

        def emit(self, record):
            """
            Emit a record.
            """
            try:
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP_SSL(self.mailhost, port)
                msg = EmailMessage()
                msg['From'] = self.fromaddr
                msg['To'] = ','.join(self.toaddrs)
                msg['Subject'] = self.getSubject(record)
                msg['Date'] = email.utils.localtime()
                msg.set_content(self.format(record))
                if self.username:
                    smtp.login(self.username, self.password)
                smtp.send_message(msg, self.fromaddr, self.toaddrs)
                smtp.quit()
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                self.handleError(record)

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

    debug_logger.addHandler(MongoHandler.to(host=mongodb_connection, db='log', collection='logs'))
    debug_logger.addHandler(ch)
    debug_logger.addHandler(mail_handler)


def init_inform_log():
    # create inform_log
    inform_logger.setLevel(logging.DEBUG)

    # mongodb debug_logger
    inform_logger.addHandler(MongoHandler.to(host=mongodb_connection, db='log', collection='logs'))
