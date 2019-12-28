# ExpirationCheck

from TimestampStore import TimestampStore
from exceptions import TransactionCollisionException
from DataStore import DataStore

class ExpirationCheck:
    def __init__(self, interval):
        self.interval = interval
        self.transaction = None

    def isExpired(self):
        timestamp, msg = TimestampStore.readTimestamp(self.transaction)
        # TODO: log msg
        return self.interval.isExpired(timestamp)

    def mark(self):
        msg = self.interval.mark()
        TimestampStore.writeTimestamp(self.transaction, msg)

    def getNext(self):
        timestamp, _ = TimestampStore.readTimestamp(self.transaction)
        return self.interval.getNext(timestamp)

    def __enter__(self):
        if self.transaction is not None:
            raise TransactionCollisionException("ExpirationCheck is already in opened transaction!")

        self.transaction = DataStore.get()
        self.transaction.open()
        return self

    def __exit__(self, type, value, tb):
        if self.transaction is None:
            raise TransactionCollisionException("ExpirationCheck is not opened!")

        self.transaction.close()
        self.transaction = None
