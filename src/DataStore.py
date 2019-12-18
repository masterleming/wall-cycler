# DataStore

import shelve
import os.path

from ConfigLoader import GlobalConfig
from exceptions import TransactionCollisionException

class DataStore:

    __instance = None

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = _DataStore(GlobalConfig.get())

        return cls.__instance


class _DataStore:
    def __init__(self, config):
        self.config = config
        self.db = None

    def __enter__(self):
        if self.db is not None:
            raise TransactionCollisionException("DB is already opened!")

        cachePath = os.path.join(self.config.cacheDir, 'wloop')
        self.db = shelve.open(cachePath)
        return self.db

    def __exit__(self, type, value, tb):
        if self.db is None:
            raise TransactionCollisionException("DB is closed!")

        self.db.close()
        self.db = None
