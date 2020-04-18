# DataStore

import shelve
import os.path

from .Config.GlobalConfig import GlobalConfig
from .exceptions import TransactionCollisionException

class DataStore: # TODO: add unit tests

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
        self.open()
        return self.db

    def __exit__(self, type, value, tb):
        self.close()

    def open(self):
        if self.db is not None:
            raise TransactionCollisionException("DB is already opened!")

        cachePath = os.path.join(self.config.cacheDir, 'wall_cycler')
        self.db = shelve.open(cachePath)

    def close(self):
        if self.db is None:
            raise TransactionCollisionException("DB is closed!")

        self.db.close()
        self.db = None
