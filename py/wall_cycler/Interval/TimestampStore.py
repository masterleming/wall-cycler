# TimestampStore

from datetime import datetime
from wall_cycler.DataStore import DataStore


class TimestampStore:
    def __init__(self, cache):
        if isinstance(cache, DataStore):
            self.dataStore = cache
        elif isinstance(cache, str):
            self.dataStore = DataStore(cache)
        else:
            raise TypeError(
                "Invalid type passed as cache! Expected 'DataStore' or path (str), got {}.".format(
                    type(cache)), cache)

    def readTimestamp(self):
        timestamp = None
        msg = None
        with self.dataStore:
            try:
                timestamp = self.dataStore['last timestamp']
                msg = self.dataStore['timestamp msg']
            except KeyError:
                pass

        return timestamp, msg

    def writeTimestamp(self, msg):
        with self.dataStore:
            self.dataStore['last timestamp'] = datetime.now()
            self.dataStore['timestamp msg'] = msg
