# TimestampStore

from datetime import datetime
from wall_cycler.DataStore import DataStore


class TimestampStore:
    def __init__(self, config):
        self.dataStore = DataStore(config)

    def readTimestamp(self):
        with self.dataStore:
            timestamp = self.dataStore['last timestamp']
            msg = self.dataStore['timestamp msg']

        return timestamp, msg

    def writeTimestamp(self, msg):
        with self.dataStore:
            self.dataStore['last timestamp'] = datetime.now()
            self.dataStore['timestamp msg'] = msg
