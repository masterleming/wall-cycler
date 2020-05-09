# DataStore

import shelve
import os.path

from .exceptions import TransactionCollisionException

DATASTORE_DB = 'cache.db'


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
        if self.db is not None:
            raise TransactionCollisionException("DB is already opened!")

        self.__ensurePathExists()

        cachePath = os.path.join(self.cacheDir, DATASTORE_DB)
        self.db = shelve.open(cachePath)

    def close(self):
        if self.db is None:
            raise TransactionCollisionException("DB is closed!")

        self.db.close()
        self.db = None

    def __getitem__(self, key):
        if self.db is None:
            with self:
                return self.__getitem__(key)
        return self.db[key]

    def __setitem__(self, key, value):
        if self.db is None:
            with self:
                return self.__setitem__(key, value)
        self.db[key] = value

    def __ensurePathExists(self):
        os.makedirs(self.cacheDir, exist_ok=True)
