# InternalScheduler

import time
from datetime import datetime, timedelta
from logging import getLogger

_logger = getLogger(__name__)


class InternalScheduler:
    def __init__(self):
        pass

    def wait(self, nextChange):
        t = self.__translateChangeTimeToAbsSeconds(nextChange)
        _logger.info("Sleeping for %d s.", t)
        time.sleep(t)

    @staticmethod
    def __translateChangeTimeToAbsSeconds(nextChange):
        return (nextChange - datetime.now()).total_seconds()
