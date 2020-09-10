# DataStore

import shelve
import os.path
from logging import getLogger

from .exceptions import TransactionCollisionException

DATASTORE_DB = 'cache.db'

_logger = getLogger(__name__)


class DataStore:
    def __init__(self, cacheDir):
        self.cacheDir = cacheDir
        self.db = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def open(self):
        _logger.info("Opening cache DB.")

        if self.db is not None:
            _logger.error("DB is already opened!")
            raise TransactionCollisionException("DB is already opened!")

        self.__ensurePathExists()

        cachePath = os.path.join(self.cacheDir, DATASTORE_DB)
        _logger.info("Using DB file: '{}'.".format(cachePath))
        self.db = shelve.open(cachePath)

    def close(self):
        _logger.info("Closing cache DB.")

        if self.db is None:
            _logger.error("DB is not opened!")
            raise TransactionCollisionException("DB is not opened!")

        self.db.close()
        self.db = None

    def __getitem__(self, key):
        _logger.debug("Retrieving value for key '%s'.", key)
        if self.db is None:
            _logger.warning("DB was not opened.")
            with self:
                return self.__getitem__(key)
        return self.db[key]

    def __setitem__(self, key, value):
        _logger.debug("Storing value for key '%s'.", key)
        if self.db is None:
            _logger.warning("DB was not opened.")
            with self:
                return self.__setitem__(key, value)
        self.db[key] = value

    def __ensurePathExists(self):
        os.makedirs(self.cacheDir, exist_ok=True)
