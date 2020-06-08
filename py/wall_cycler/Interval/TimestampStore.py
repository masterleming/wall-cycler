# TimestampStore

from datetime import datetime
from logging import getLogger

from wall_cycler.DataStore import DataStore

_logger = getLogger(__name__)


class TimestampStore:
    def __init__(self, cache):
        _logger.debug("Initialising.")
        if isinstance(cache, DataStore):
            _logger.debug("Using DataStore instance")
            self.dataStore = cache
        elif isinstance(cache, str):
            _logger.debug("Creating new DataStore from path: '%s'.", cache)
            self.dataStore = DataStore(cache)
        else:
            _logger.error("Unsupported cache type! Type: '%s', str(%s).", type(cache), cache)
            raise TypeError(
                "Invalid type passed as cache! Expected 'DataStore' or path (str), got {}.".format(
                    type(cache)), cache)

    def readTimestamp(self):
        _logger.debug("Reading timestamp from cache.")
        timestamp = None
        msg = None
        with self.dataStore:
            try:
                timestamp = self.dataStore['last timestamp']
                msg = self.dataStore['timestamp msg']
            except KeyError:
                _logger.warning("Cache does not contain timestamp. Using defaults.")
                pass

        _logger.debug("Timestamp: '%s', message: '%s'.", timestamp, msg)
        return timestamp, msg

    def writeTimestamp(self, msg):
        now = datetime.now()

        _logger.debug("Writing timestamp: '%s', with message '%s'.", now, msg)

        with self.dataStore:
            self.dataStore['last timestamp'] = now
            self.dataStore['timestamp msg'] = msg
