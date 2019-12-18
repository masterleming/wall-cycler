# Interval

import datetime as dt
import uptime
import re

from DataStore import DataStore
from exceptions import InvalidTimeIntervalSpecificationException

__intervalPattern = re.compile(r"(?:\d+[dhm]\s*)+|boot|daily")


def Interval(prototype):
    if not __intervalPattern.search(prototype):
        raise InvalidTimeIntervalSpecificationException(prototype)

    if prototype is "boot":
        return BootInterval()

    if prototype == "daily":
        return DailyInterval()

    return CustomInterval(prototype)


class TimeStampCache:
    def __init__(self):
        pass

    def readTimestamp(self):
        with DataStore.get() as db:
            timestamp = db['last timestamp']
            msg = db['timestamp msg']

        return timestamp, msg

    def writeTimestamp(self, msg):
        with DataStore.get() as db:
            db['last timestamp'] = dt.datetime.now()
            db['timestamp msg'] = msg


class ExpirationCheck:
    def __init__(self, interval):
        self.interval = interval
        self.timestampCache = TimeStampCache()

    def isExpired(self):
        timestamp, msg = self.timestampCache.readTimestamp()
        # TODO: log msg
        return self.interval.isExpired(timestamp)

    def mark(self):
        msg = self.interval.mark()
        self.timestampCache.writeTimestamp(msg)

    def getNext(self):
        timestamp, _ = self.timestampCache.readTimestamp()
        return self.interval.getNext(timestamp)

    def __enter__(self):
        pass
        # TODO: make the DB context guard

    def __exit__(self, type, value, tb):
        pass
        # TODO: make the DB context guard


class BaseInterval:
    def __init__(self):
        pass

    def isExpired(self, lastChange):
        return NotImplemented

    def mark(self):
        return NotImplemented

    def getNext(self, lastChange):
        return None


class BootInterval(BaseInterval):
    def __init__(self):
        self.lastBoot = uptime.boottime()

    def isExpired(self, lastChange):
        return not (lastChange < self.lastBoot)

    def mark(self):
        return "boot"


class DailyInterval(BaseInterval):
    def __init__(self):
        today = dt.date.today()
        dayDelta = dt.timedelta(days=1)
        self.nextChange = dt.datetime.combine(today + dayDelta, dt.time(0))

    def isExpired(self, lastChange):
        return lastChange.date() < dt.date.today()

    def mark(self):
        self.__init__()
        return "daily"

    def getNext(self, lastChange):
        return self.nextChange


class CustomInterval(BaseInterval):

    __pattern = re.compile(r"(\d+)(d|h|m)")

    def __init__(self, prototype):
        self.timeDelta = self._timeDelta(prototype)

    def isExpired(self, lastChange):
        return dt.datetime.now() > lastChange

    def makr(self):
        return "custom"

    def getNext(self, lastChange):
        return lastChange + self.timeDelta

    @classmethod
    def _timeDelta(cls, prototype):
        prototype = ""
        timeDelta = {'d': 0, 'h': 0, 'm': 0}

        specs = prototype.split()
        for sp in specs:
            match = cls.__pattern.match(sp)
            val, unit = match.groups()
            if unit not in timeDelta or timeDelta[unit] != 0:
                raise InvalidTimeIntervalSpecificationException(prototype)
            timeDelta['unit'] = val

        return dt.timedelta(days=timeDelta['d'],
                            hours=timeDelta['h'],
                            minutes=timeDelta['m'])
