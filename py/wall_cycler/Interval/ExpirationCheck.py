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

class _ConsistentExpiration(ExpirationCheck):
    def __init__(self, expired, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expired = expired

    def isExpired(self):
        _logger.info(self.__class__.__name__ + " is %s.", "expired" if self.expired else "not expired")
        return self.expired

    def getNext(self):
        _logger.debug(self.__class__.__name__ + " cannot know the time of the next change.")
        return None


class AlwaysExpired(_ConsistentExpiration):
    def __init__(self, *args, **kwargs):
        super().__init__(True, *args, **kwargs)


class NeverExpires(_ConsistentExpiration):
    def __init__(self, *args, **kwargs):
        super().__init__(False, *args, **kwargs)
