# ExpirationCheck

from .TimestampStore import TimestampStore
from wall_cycler.exceptions import TransactionCollisionException
from wall_cycler.DataStore import DataStore


class ExpirationCheck:
    def __init__(self, interval, timestampStore):
        self.interval = interval
        self.timestampStore = timestampStore

    def isExpired(self):
        timestamp, msg = self.timestampStore.readTimestamp()
        # TODO: log msg

        if timestamp is None:
            return True
        return self.interval.isExpired(timestamp)

    def mark(self):
        msg = self.interval.mark()
        self.timestampStore.writeTimestamp(msg)

    def getNext(self):
        timestamp, _ = self.timestampStore.readTimestamp()
        return self.interval.getNext(timestamp)
