# -*- coding: utf-8 *-*
import getpass
import logging
import sys
from datetime import datetime

from _socket import gethostname
from pymongo import MongoClient as Connection

if sys.version_info[0] >= 3:
    unicode = str


class MongoFormatter(logging.Formatter):
    def format(self, record):
        """Format exception object as a string"""
        data = record.__dict__.copy()

        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg

        data.update(
            username=getpass.getuser(),
            time=datetime.now(),
            host=gethostname(),
            message=msg,
            args=tuple(unicode(arg) for arg in record.args)
        )
        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])
        return data


class MongoHandler(logging.Handler):
    """ Custom log handler

    Logs all messages to a mongo collection. This  handler is
    designed to be used with the standard python logging mechanism.
    """

    @classmethod
    def to(cls, collection: str, db='log', host='localhost', port=None,
           username=None, password=None, level=logging.NOTSET):
        """ Create a handler for a given  """
        return cls(collection, db, host, port, username, password, level)

    def __init__(self, collection: str, db='log', host='localhost', port=None,
                 username=None, password=None, level=logging.NOTSET):
        """ Init log handler and store the collection handle """
        logging.Handler.__init__(self, level)
        connection = Connection(host, port)
        if username and password:
            connection[db].authenticate(username, password)
        self.collection = connection[db][collection]
        self.formatter = MongoFormatter()

    def emit(self, record):
        """ Store the record to the collection. Async insert """
        try:
            self.collection.insert_one(self.format(record))
        except Exception as e:
            logging.error("Unable to save log record: %s", str(e),
                          exc_info=True)
