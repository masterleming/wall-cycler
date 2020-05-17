# InternalScheduler

import time
from datetime import datetime, timedelta

class InternalScheduler:
    def __init__(self):
        pass

    def wait(self, nextChange):
        time.sleep(self.__translateChangeTimeToAbsSeconds(nextChange))

    @staticmethod
    def __translateChangeTimeToAbsSeconds(nextChange):
        return (nextChange - datetime.now()).total_seconds()
