# ExpirationCheck

from logging import getLogger

from .TimestampStore import TimestampStore
from ..exceptions import TransactionCollisionException
from ..DataStore import DataStore

_logger = getLogger(__name__)


class ExpirationCheck:
    def __init__(self, interval, timestampStore):
        self.interval = interval
        self.timestampStore = timestampStore

    def isExpired(self):
        _logger.info("Checking expiration.")

        timestamp, msg = self.timestampStore.readTimestamp()
        _logger.debug("Read timestamp: '{}' with message: '{}' from cache.".format(timestamp, msg))

        if timestamp is None:
            _logger.debug("No timestamp defaults to 'expired'.")
            return True

        expired = self.interval.isExpired(timestamp)
        _logger.info("Expired? %s.", "Yes" if expired else "No")
        return expired

    def mark(self):
        _logger.debug("Marking current time as time of the last change.")
        msg = self.interval.mark()
        self.timestampStore.writeTimestamp(msg)

    def getNext(self):
        _logger.debug("Obtaining time of the next change (if possible).")

        timestamp, _ = self.timestampStore.readTimestamp()
        nextChange = self.interval.getNext(timestamp)

        _logger.debug("Next change at: %s.", nextChange)
        return nextChange
